from django.urls import path
from . import views

urlpatterns = [
	path('', views.Mainpage.as_view(), name = 'mainpage'),
    path('articles/', views.ArticlesList.as_view(), name = 'articles_list'),
    path('form/', views.UrlAndPriceForm.as_view(), name = "formview"),
    path('price/<slug>/', views.first_scrape, name = 'pricescraper'),
    path('product/remove/<slug:product>', views.product_remove, name = 'product_remove')
]