from celery import shared_task
from .models import Product
from .scrapers import scraping, articles_scraper

@shared_task
def init_scraping():

	products = Product.objects.filter(ended = False)
	for product in products:
		product = product.slug
		scraping.delay(product)

@shared_task
def article_scrape():
	articles_scraper()


