from django.urls import path
from apps.sync1c import views


app_name = 'sync1c'


urlpatterns = [
    path('',  views.updateFrom1C.as_view()),
]
