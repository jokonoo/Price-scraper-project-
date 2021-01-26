from django.urls import path
from .views import UserCreationView, UserProducts, DetailedProduct
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
	path('register/', UserCreationView.as_view(), name = 'register'),
	path('login/', LoginView.as_view(template_name = 'user/login.html'), name = 'login'),
	path('logout/', LogoutView.as_view(template_name = 'user/logout.html'), name = 'logout'),
	path('products/', UserProducts.as_view(), name = 'user_products'),
	path('products/<slug:slug>', DetailedProduct.as_view(), name = 'detailed_product')
]