from rest_framework import serializers
from .models import ProductTransaction

class ProductTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTransaction
        fields = '__all__'