from django.shortcuts import render
from main.models import Product
from .serializers import ProductSerializer, ArticleSerializer
from rest_framework import generics

class ProductListApi(generics.ListCreateAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

class ProductDetailApi(generics.RetrieveUpdateDestroyAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	lookup_field = 'slug'



