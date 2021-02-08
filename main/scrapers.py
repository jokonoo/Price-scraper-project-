import os
import requests
from bs4 import BeautifulSoup as bs
from.models import Article, Product
from django.core.mail import send_mail
from celery import shared_task

'''
At first i used selenium to scrape the content from site, but it last too long(around 5 seconds per one request).
I decided to use bs4 because it is much faster, and i personally thought that it should be better
for my purposes. Function below works as it should, but it is really much slower,
than scraping with bs4.
'''
def first_scrape(slug):

	object = Product.objects.get(slug = slug)
	if 'www.morele.net' in object.url:
		response = requests.get(object.url).text
		source = bs(response, 'lxml')
		name = source.select('h1.prod-name')[0].string
		price = source.select('div.product-price')[0].text

		try:
			not_available = source.select('div.product-box-main__add-to-cart')[0].text
			
			if 'PRODUKT NIEDOSTĘPNY' in not_available:
				object.delete()
				object = False
			
			else:
				raise Exception('')
		
		except:
			
			try:
				not_available = source.select('div.product-price.product-price--small')[0].text
			
				if 'w outlecie od' in not_available:
					object.delete()
					object = False

			except:
				pass
		
		finally:
			if object == False:
				return "error"
			else:
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

@shared_task
def scraping(product):
	
	#PRODUCT OBJECT
	product = Product.objects.get(slug = product)
	#PRODUCT NOT AVAILABLE CASE MESSAGE
	product_not_available_subject = 'Product not available in shop'
	product_not_available_message = f'Item that You are tracking: {product.name}, is not available in shop morele.pl anymore.'
	#PRICE OF PRODUCT DROPPED CASE MESSAGE
	product_price_dropped_subject = 'Price dropped!!!'
	product_price_dropped_message = f'Item that You are tracking: {product.name}, just dropped under wanted price of: {product.wanted_price} zł'
	
	#CHECKING IF URL OF THE PRODUCT IS MORELE
	if 'www.morele.net' in product.url:
		response = requests.get(product.url).text
		source = bs(response, 'lxml')
		price = source.select('div.product-price')[0].text
		
		#CHECKING IF THE PRODUCT IS NOT AVAILABLE IN TWO DIFFERENT CASES
		try:
			not_available = source.select('div.product-box-main__add-to-cart')[0].text
			
			if 'PRODUKT NIEDOSTĘPNY' in not_available:
				product.ended = True
				product.save()
				send_mail(
					subject = product_not_available_subject,
					message = product_not_available_message,
					recipient_list = [str(product.user.email)],
					from_email = os.environ.get('EMAIL_USER')
					)
			
			else:
				raise Exception('')
		
		except:
			
			try:
				not_available = source.select('div.product-price.product-price--small')[0].text
			
				if 'w outlecie od' in not_available:
					product.ended = True
					product.save()
					send_mail(
						subject = product_not_available_subject,
						message = product_not_available_message,
						recipient_list = [str(product.user.email)],
						from_email = os.environ.get('EMAIL_USER')
						)
			except:
				pass
		
		#FINALLY IF PRODUCT IS AVAILABLE CHECKING IF PRICE OF THE PRODUCT DROPPED AND WANTED VALUE
		finally:
			if product.ended == True:
				return
			
			if ',' in price:
					price = ''.join(price.strip().split())
					price = int(''.join(price.split(','))[0:-4])
					
					if price < product.current_price:
						product.current_price = price
						product.save()
						
						if product.wanted_price >= product.current_price:
							product.ended = True
							product.save()
							send_mail(
								subject = product_price_dropped_subject,
								message = product_price_dropped_message,
								recipient_list = [str(product.user.email)],
								from_email = os.environ.get('EMAIL_USER')
								)
					
					elif price > product.current_price:
						product.current_price = price
						product.save()
			
			else:	
					price = int(''.join(price.strip().split())[0:-2])
					
					if price < product.current_price:
						product.current_price = price
						product.save()
						
						if product.wanted_price >= product.current_price:
							product.ended = True
							product.save()
							send_mail(
								subject = product_price_dropped_subject,
								message = product_price_dropped_message,
								recipient_list = [str(product.user.email)],
								from_email = os.environ.get('EMAIL_USER')
								)
					
					elif price > product.current_price:
						product.current_price = price
						product.save()

def articles_scraper():
	mainpage_url = 'https://lowcygier.pl/'
	#variable with mainpage url of site that i'm scraping from
	URL = f'{mainpage_url}darmowe/'
	#variable with exact url of page that i'm scraping from
	category = 'games'
	#variable with category to help with filtering
	
	data = requests.get(URL).text
	source = bs(data, 'lxml')
	source = source.find_all('article')
	for article in source[::-1]:
		link = article.find('header').find('h2', class_= 'post-title').a['href']
		header = article.find('header').find('h2', class_= 'post-title').text
		header = header.strip()
		object, created = Article.objects.get_or_create(
			url = link,
			title = header,
			category = category,
			defaults = {'mainpage_url' : mainpage_url}
			)