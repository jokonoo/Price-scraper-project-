from main.models import Product, Article
from .serializers import ProductSerializer, ArticleSerializer
from rest_framework import generics, filters

class ProductListApi(generics.ListCreateAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['name', 'url', 'user__username']

class ProductDetailApi(generics.RetrieveUpdateDestroyAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	lookup_field = 'slug'

class ArticleListApi(generics.ListCreateAPIView):
	queryset = Article.objects.all()
	serializer_class = ArticleSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'url', 'category', 'mainpage_url']

class ArticleDetailApi(generics.RetrieveUpdateDestroyAPIView):
	queryset = Article.objects.all()
	serializer_class = ArticleSerializer




