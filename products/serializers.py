from rest_framework import serializers
from .models import Product
from categories.models import Category

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'description', 'price', 'image', 'created_at']
        read_only_fields = ['created_at']
