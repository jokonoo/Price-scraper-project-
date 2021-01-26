import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'public.settings')
app = Celery('public')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
	'automated_scraping' : {
		'task' : 'main.tasks.init_scraping',
		'schedule' : crontab(minute='*/15')
	},
	'articles_scraping' : {
		'task' : 'main.tasks.article_scrape',
		'schedule' : crontab(minute=0, hour='*/1')
	}
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')