from django.db.models import signals
from django.urls import include, path, re_path
from apps.core import views


app_name = 'core'

urlpatterns = [
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('recall',      views.recall,  name='recall'),
    path('set_language/<language>/', views.set_language, name="set_language")
]
