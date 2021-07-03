from django.urls import include, path, re_path
from django.views.generic import TemplateView
from apps.pages import views


app_name = 'pages'


urlpatterns = [
    path('about/',                views.page_about,     name='about'),
    path('contacts/',             views.ContactFormView.as_view(), name='contacts'),
    path('contacts/successs/',    TemplateView.as_view(template_name="pages/success.html")),
    path('delivery/',             views.page_payment, name='payment'),
    path('payment/',              views.page_delivery, name='delivery'),
    path('terms-of-use/',         views.page_terms_of_use, name='terms_of_use'),

    path('<slug>/', views.PageDetailView.as_view(),     name='page')

   
]
