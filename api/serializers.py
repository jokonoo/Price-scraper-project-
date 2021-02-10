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
		'first_price',
		'current_price',
		'wanted_price',
		'date',
		'ended',
		'user',
		]

class ArticleSerializer(serializers.HyperlinkedModelSerializer):

	hyperlink = serializers.HyperlinkedIdentityField(
		view_name='article_detail',
		lookup_field = 'pk'
		)
		
	class Meta:
		model = Article
		fields = [
		'hyperlink',
		'title',
		'url',
		'date',
		'category',
		'mainpage_url',
		]