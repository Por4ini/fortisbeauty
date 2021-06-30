from django.urls import path, re_path, include
from django.contrib.auth import views as authViews
from django.views.generic import TemplateView
from apps.user.forms import PasswordRestoreForm
from . import views

app_name = 'user'


profile = [
    path('',                 views.user_data,            name='profile'),
    path('orders/',          views.user_orders,          name='user_orders'),
    path('wishlist/',        views.user_wishlist,        name='user_wishlist'),
    path('company/',         views.user_company,         name='user_company'),
    path('comments/',        views.user_comments,        name='user_comments'),
    path('questions/',       views.user_questions,       name='user_questions'),
    path('logout/',          views.user_logout,          name='user_logout'),
    path('password_change/', views.user_password_change, name='user_password_change'),
    
]


registration = [
    path('',                   views.CustomerRegistration.as_view(), name='registration'),
    path('business/',          views.PartnerRegistration.as_view(),  name='registration_business'),
    path('success/',           TemplateView.as_view(template_name="user/registration/customer/success.html"), name='registration_success'),
    path('business/success/',  TemplateView.as_view(template_name="user/registration/partner/success.html"),  name='registration_business_success'),
]


pssword_restore = [
    path(
        'html/', TemplateView.as_view(
            template_name = 'user/password_restore/email_template.html',
        ), 
        kwargs={'uidb64' : '123123', 'token' : '1232'},
        name='restore_password__success',
    ),
   
    path(
        '',                        
        authViews.PasswordResetView.as_view(
            form_class =    PasswordRestoreForm,
            template_name = 'user/password_restore/form.html',
            from_email =    'office.fortisbeauty@gmail.com',
            success_url =   '/restore_password/success/',
        ), 
        name='restore_password'
    ),
    path(
        'success/',                
        TemplateView.as_view(
            template_name = 'user/password_restore/success.html'
        ), 
        name='restore_password__success'
    ),
    path(
        'done/', 
        authViews.PasswordResetDoneView.as_view(), 
        kwargs={'template_name': 'user/password_restore/done.html'}, 
        name='restore_password__done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        authViews.PasswordResetConfirmView.as_view(
            template_name = 'user/password_restore/link_form.html',
            success_url =   '/login',
        ),
        name='restore_password__confirm'
    ),
]


urlpatterns = [
    path('login/',   views.LoginView.as_view(),  name='login'),
    path('logout/',  views.user_logout,          name='logout'),
    path('profile/',           include(profile)),
    path('restore_password/',  include(pssword_restore)),
    path('registration/',      include(registration)),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),  
]
