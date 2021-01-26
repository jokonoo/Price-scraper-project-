from django.shortcuts import render
from django.views.generic import FormView, ListView, DetailView
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from main.models import Product

class UserCreationView(FormView):
	
	template_name = 'user/registration.html'
	form_class = UserRegisterForm
	
	def form_valid(self,form):
		form.save()
		return HttpResponseRedirect(reverse('mainpage'))

class UserProducts(ListView):
	
	model = Product
	template_name = 'user/products.html'
	paginate_by = 20

	def get_context_data(self):
		context = super().get_context_data()
		context['p_not_ended'] = Product.objects.filter(user = self.request.user, ended = False)
		context['p_ended'] = Product.objects.filter(user = self.request.user, ended = True)
		return context

class DetailedProduct(DetailView):

	model = Product
	template_name = 'user/product_info.html'
	context_object_name = 'product'





