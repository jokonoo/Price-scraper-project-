from rest_framework import serializers
from main.models import Product, Article

class ProductSerializer(serializers.ModelSerializer):
	
	user = serializers.StringRelatedField()
	hyperlink = serializers.HyperlinkedIdentityField(
		view_name='product_detail',
		lookup_field = 'slug'
		)
		
	class Meta:
		model = Product
		fields = [
		'hyperlink',
		'name',
		'url',
		'slug',
		'first_price',
		'current_price',
		'wanted_price',
		'date',
		'image_url',
		'ended',
		'user']

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
		
	class Meta:
		model = Article
		exclude = ['image']