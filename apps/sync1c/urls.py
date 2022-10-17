from django.urls import path, include
from apps.sync1c import views



app_name = 'sync1c'



urlpatterns = [
    #path('', include(router.urls)),
    path('',  views.updateFrom1C.as_view()),
]
