from django.urls import path
from . import views

urlpatterns = [
	path('products/',views.ProductListApi.as_view(), name = 'product_list'),
	path('products/<slug:slug>', views.ProductDetailApi.as_view(), name = 'product_detail')
]