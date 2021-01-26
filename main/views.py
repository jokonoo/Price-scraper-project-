#django imports
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, FormView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, Product
from .forms import UrlForm

# requests/bs4 imports
import requests
from bs4 import BeautifulSoup as bs

class Mainpage(TemplateView):
	template_name = 'main/mainpage.html'

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
		 first_scrape(object.slug)
		 #return HttpResponseRedirect(reverse(first_scrape, kwargs = {'slug' : object.slug}))
		 return HttpResponseRedirect(reverse('mainpage'))

def first_scrape(slug):

	object = Product.objects.get(slug = slug)
	if 'www.morele.net' in object.url:
		response = requests.get(object.url).text
		source = bs(response, 'lxml')
		name = source.select('h1.prod-name')[0].string
		price = source.select('div.product-price')[0].text
		if ',' in price:
			price = ''.join(price.strip().split())
			price = int(''.join(price.split(','))[0:-4]) 
		else:
			price = int(''.join(price.strip().split())[0:-2])
		
		object, created = Product.objects.get_or_create(
			url = object.url,
			wanted_price = object.wanted_price,
			defaults = {'name' : name, 'first_price' : price, 'current_price' : price}
			)
		if object:
			object.name = name
			object.first_price = price
			object.current_price = price
			object.save()