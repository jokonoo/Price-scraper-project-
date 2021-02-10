from django.urls import path
from . import views

urlpatterns = [
	path('products/',views.ProductListApi.as_view(), name = 'product_list'),
	path('products/<slug:slug>/', views.ProductDetailApi.as_view(), name = 'product_detail'),
	path('articles/', views.ArticleListApi.as_view(), name = 'article_list'),
	path('articles/<pk>/', views.ArticleDetailApi.as_view(), name = 'article_detail'),
	
]