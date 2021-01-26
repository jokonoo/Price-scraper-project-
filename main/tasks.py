from celery import shared_task
from celery.schedules import crontab
from .models import Product
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .scrapers import scraping, articles_scraper


#def scraping(url):
	
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
#				#sendmail that price dropped under wanted price
#		elif price > product.current_price:
#			product.current_price = price
#			product.save()
#		product.worked = True
#		product.save()
#		driver.close()

@shared_task
def init_scraping():

	products = Product.objects.filter(ended = False)
	for product in products:
		scraping(product)

@shared_task
def article_scrape():
	articles_scraper()


