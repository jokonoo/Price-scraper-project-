from django.db import models
from PIL import Image
from django.contrib.auth.models import User

class Article(models.Model):
	title = models.CharField(max_length = 500, null = True, blank = True)
	url = models.URLField()
	date = models.DateTimeField(auto_now_add = True)
	image = models.ImageField(upload_to = 'ArticlePicture', default = 'default.jpg', null = True, blank = True)
	image_url = models.URLField(null = True, blank = True)
	category = models.CharField(max_length = 50, null = True, blank = True)
	mainpage_url = models.URLField(null = True, blank = True)

	class Meta:
		ordering = ['-date']

class Product(models.Model):
	name = models.CharField(max_length = 250, null = True, blank = True)
	slug = models.SlugField(max_length = 250, null = True, blank = True)
	url = models.URLField(null = True, blank = True)
	first_price = models.IntegerField(null = True, blank = True)
	current_price = models.IntegerField(null = True, blank = True)
	wanted_price = models.IntegerField(default = 100, null = True, blank = True)
	date = models.DateTimeField(auto_now_add = True)
	image_url = models.URLField(null = True, blank = True)
	ended = models.BooleanField(default = False)
	user = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True)

	#def save(self, *args, **kwargs):
	#	self.slug = f'{self.pk}_{self.wanted_price}'
	#	super().save()
	
	class Meta:
		ordering = ['ended', '-date']

