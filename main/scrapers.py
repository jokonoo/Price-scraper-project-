import requests
from bs4 import BeautifulSoup as bs
from.models import Article, Product
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.core.mail import send_mail
import os

'''
At first i used selenium to scrape the content from site, but it last too long(around 5 seconds).
I decided to use bs4 because it is much faster, and i personally thought that it should be better
for my purposes. Function below works as it should, but it is really much slower,
than scraping with bs4.
'''
def scraping(product):

	if 'www.morele.net' in product.url:
		response = requests.get(product.url).text
		source = bs(response, 'lxml')
		price = source.select('div.product-price')[0].text
		
		if ',' in price:
			price = ''.join(price.strip().split())
			price = int(''.join(price.split(','))[0:-4]) 
		else:
			price = int(''.join(price.strip().split())[0:-2])
		
		if price < product.current_price:
			product.current_price = price
			product.save()
			if product.wanted_price >= product.current_price:
				product.ended = True
				product.save()
				send_mail(
					subject = 'Price drop!!!',
					message = f'Item that You are tracking: {product.name}, just dropped under wanted price of: {product.wanted_price} zł',
					recipient_list = [str(product.user.email)],
					from_email = os.environ.get('EMAIL_USER')
					)
		elif price > product.current_price:
			product.current_price = price
			product.save()
		
		product.worked = True
		product.save()

#def scraping(product):
#	
#	PATH = 'C:\Program Files (x86)\chromedriver.exe'
#	chrome_options = Options()
#	chrome_options.add_argument('--headless')
#	driver = webdriver.Chrome(PATH)
#	if 'www.morele.net' in product.url:
#		driver.get(product.url)
#		price = driver.find_element_by_id('product_price_brutto').text[0:-2]
#		price = int("".join(price.split()))
#		if price < product.current_price:
#			product.current_price = price
#			product.save()
#			if product.wanted_price >= product.current_price:
#				product.ended = True
				#sendmail that price dropped under wanted price
#		elif price > product.current_price:
#			product.current_price = price
#			product.save()
#		product.worked = True
#		product.save()
#		driver.close()

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
		object, created = Article.objects.get_or_create(
			url = link,
			title = header,
			category = category,
			defaults = {'mainpage_url' : mainpage_url}
			)