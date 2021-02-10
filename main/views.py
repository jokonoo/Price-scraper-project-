#django imports
from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Article, Product
from .forms import UrlForm
from .scrapers import first_scrape
from django.contrib import messages

# requests/bs4 imports
import requests
from bs4 import BeautifulSoup as bs

class Mainpage(ListView):
	model = Article
	template_name = 'main/mainpage.html'

	def get_context_data(self):
		context = super().get_context_data()
		context['articles'] = Article.objects.all()[0:3]
		context['products'] = Product.objects.all()[0:3]
		return context

class ArticlesList(ListView):
	model = Article
	template_name = 'main/articles.html'
	context_object_name = 'articles'
	paginate_by = 20

class UrlAndPriceForm(LoginRequiredMixin, FormView):
	template_name = 'main/urlform.html'
	form_class = UrlForm

	def form_valid(self, form):
		 url = form.cleaned_data['url']
		 price = form.cleaned_data['price']
		 object, created = Product.objects.get_or_create(
		 	url = url,
		 	user = self.request.user,
		 	ended = False,
		 	defaults = {'wanted_price' : price})
		 msg = first_scrape(object.slug)
		 if msg == "error":
		 	messages.error(self.request, 'Item is not available')
		 return redirect('mainpage')

def product_remove(request, product):
	instance = Product.objects.get(slug = product)
	instance.delete()
	messages.info(request, 'Product removed successfully')
	return redirect('user_products')
