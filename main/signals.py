from django.db.models.signals import post_save
from .models import Product
from django.dispatch import receiver

@receiver(post_save, sender = Product)
def create_slug(sender, instance, created, **kwargs):
	if created:
		var = str(instance.wanted_price)
		instance.slug = f'{instance.id}_{var}'
		instance.save() 