from django.urls import path
from .views import initialize_database,ProductTransactionList,statistics,bar_chart,pie_chart,combined_data

urlpatterns = [
    path('initialize/',initialize_database,name='initialize-database'),
    path('transactions/', ProductTransactionList.as_view(), name='transaction-list'),
    path('statistics/', statistics, name='statistics'),
    path('bar-chart/', bar_chart, name='bar-chart'),
    path('pie-chart/', pie_chart, name='pie-chart'),
    path('combined-data/', combined_data, name='combined-data'),
]