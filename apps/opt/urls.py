from django.urls import include, path, re_path

from apps.opt import views
from django.views.generic import TemplateView

app_name = 'opt'

urlpatterns = [
    path('',               views.WhoosaleView.as_view(), name='opt'),
    path('success/',       TemplateView.as_view(template_name="opt/success.html"), name='success'),
    path('offer/',         TemplateView.as_view(template_name="opt/salons/main.html"), name='opt_offer'),
    path('offer/quiz/',    views.SalonsView.as_view(),   name='opt_offer_quiz'),
    # path('get_analitics/', views.get_analitics, name='get_analitics'),
]