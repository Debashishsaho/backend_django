from django.shortcuts import render
import requests
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics
from .models import ProductTransaction
from .serializers import ProductTransactionSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum, Count
import datetime

THIRD_PARTY_API_URL = "https://s3.amazonaws.com/roxiler.com/product_transaction.json"


@api_view(['GET'])
def initialize_database(request):
    response=requests.get(THIRD_PARTY_API_URL)
    if response.status_code==200:
        data=response.json()
        for item in data:
            date_of_sale = datetime.datetime.strptime(item['dateOfSale'], '%Y-%m-%dT%H:%M:%S%z').date()
            ProductTransaction.objects.create(
                title=item['title'],
                price=item['price'],
                description=item['description'],
                category=item['category'],
                sold=item['sold'],
                date_of_sale=date_of_sale,
            )
        return Response({"status": "Database initialized with seed data"}, status=status.HTTP_201_CREATED)
    return Response({"error": "Failed to fetch data"}, status=status.HTTP_400_BAD_REQUEST)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductTransactionList(generics.ListAPIView):
    serializer_class = ProductTransactionSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = ProductTransaction.objects.all()
        month = self.request.query_params.get('month')
        search = self.request.query_params.get('search')
        if month:
            queryset = queryset.filter(date_of_sale__month=datetime.datetime.strptime(month, '%B').month)
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(description__icontains=search) |
                models.Q(price__icontains=search)
            )
        return queryset

@api_view(['GET'])
def statistics(request):
    month = request.query_params.get('month')
    if not month:
        return Response({"error": "Month is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    month_number = datetime.datetime.strptime(month, '%B').month
    total_sale_amount = ProductTransaction.objects.filter(date_of_sale__month=month_number, sold=True).aggregate(Sum('price'))['price__sum']
    total_sold_items = ProductTransaction.objects.filter(date_of_sale__month=month_number, sold=True).count()
    total_not_sold_items = ProductTransaction.objects.filter(date_of_sale__month=month_number, sold=False).count()

    return Response({
        "total_sale_amount": total_sale_amount,
        "total_sold_items": total_sold_items,
        "total_not_sold_items": total_not_sold_items
    })

@api_view(['GET'])
def bar_chart(request):
    month = request.query_params.get('month')
    if not month:
        return Response({"error": "Month is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    month_number = datetime.datetime.strptime(month, '%B').month
    price_ranges = [
        ('0-100', 0, 100), ('101-200', 101, 200), ('201-300', 201, 300),
        ('301-400', 301, 400), ('401-500', 401, 500), ('501-600', 501, 600),
        ('601-700', 601, 700), ('701-800', 701, 800), ('801-900', 801, 900),
        ('901-above', 901, float('inf'))
    ]
    
    data = {}
    for label, lower, upper in price_ranges:
        count = ProductTransaction.objects.filter(
            date_of_sale__month=month_number,
            price__gte=lower,
            price__lte=upper if upper != float('inf') else 999999
        ).count()
        data[label] = count

    return Response(data)


@api_view(['GET'])
def pie_chart(request):
    month = request.query_params.get('month')
    if not month:
        return Response({"error": "Month is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    month_number = datetime.datetime.strptime(month, '%B').month
    categories = ProductTransaction.objects.filter(date_of_sale__month=month_number).values('category').annotate(count=Count('category'))

    return Response({item['category']: item['count'] for item in categories})


@api_view(['GET'])
def combined_data(request):
    month = request.query_params.get('month')
    if not month:
        return Response({"error": "Month is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Statistics
    month_number = datetime.datetime.strptime(month, '%B').month
    total_sale_amount = ProductTransaction.objects.filter(date_of_sale__month=month_number, sold=True).aggregate(Sum('price'))['price__sum']
    total_sold_items = ProductTransaction.objects.filter(date_of_sale__month=month_number, sold=True).count()
    total_not_sold_items = ProductTransaction.objects.filter(date_of_sale__month=month_number, sold=False).count()

    statistics_data = {
        "total_sale_amount": total_sale_amount,
        "total_sold_items": total_sold_items,
        "total_not_sold_items": total_not_sold_items
    }

    # Bar Chart Data
    price_ranges = [
        ('0-100', 0, 100), ('101-200', 101, 200), ('201-300', 201, 300),
        ('301-400', 301, 400), ('401-500', 401, 500), ('501-600', 501, 600),
        ('601-700', 601, 700), ('701-800', 701, 800), ('801-900', 801, 900),
        ('901-above', 901, float('inf'))
    ]

    bar_chart_data = {}
    for label, lower, upper in price_ranges:
        count = ProductTransaction.objects.filter(
            date_of_sale__month=month_number,
            price__gte=lower,
            price__lte=upper if upper != float('inf') else 999999
        ).count()
        bar_chart_data[label] = count

    # Pie Chart Data
    categories = ProductTransaction.objects.filter(date_of_sale__month=month_number).values('category').annotate(count=Count('category'))
    pie_chart_data = {item['category']: item['count'] for item in categories}

    combined_response = {
        "statistics": statistics_data,
        "bar_chart": bar_chart_data,
        "pie_chart": pie_chart_data
    }

    return Response(combined_response)


