from django.contrib.auth import login
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, FormView
from django.utils.encoding import force_text
from django.contrib.auth.tokens import PasswordResetTokenGenerator  
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import six
from apps.user.tokens import TokenGenerator
from apps.user.forms import UserRegistrationForm, BusinessUserFormSetFactory, BusinessUserForm
from apps.user.models import CustomUser
from apps.core.functions import send_telegeram
import json




def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = CustomUser.objects.get(pk=uid)

    if user is not None and TokenGenerator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('shop:home')
    else:
        return HttpResponse('Ссылка активации не верна')




class CustomerRegistration(CreateView):
    form = UserRegistrationForm
    form_class = UserRegistrationForm
    model = CustomUser
    success_url =   '/registration/success'
    template_name = 'user/registration/customer/form.html'

    
    def send_activation(self):
        user = self.object
        mail_subject = 'Активируйте Вашу учетныую запись FortisBeuty.'
    
        html = render_to_string('user/email/acc_activation_email.html', context={
                'user': user,
                'domain': self.request.META['HTTP_HOST'],
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }, 
        )
        email = EmailMessage(
            mail_subject,
            html,
            'office.fortisbeauty@gmail.com',
            [user.email],
            headers={
                'Reply-To': 'office.fortisbeauty@gmail.com'
            }
        )
        email.content_subtype = "html"
        email.send()


    def get(self, request):
        if request.user.is_authenticated:
            return redirect('user:profile')
        return render(request, self.template_name, {'form': self.form})


    def form_valid(self, form):
        result = super(CustomerRegistration, self).form_valid(form)
        self.send_activation()
        return result
  



class PartnerRegistration(CreateView):
    form = BusinessUserForm
    form_class = BusinessUserForm
    model = CustomUser
    success_url =   '/registration/business/success/'
    template_name = 'user/registration/partner/from.html'

    def send_to_telegram(self):
        obj = self.object
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
        msg = [
            'Регистрация оптового покупателя.' + '\n',
            ' '.join([obj.first_name,obj.father_name,obj.last_name]),
            'Город: ' + obj.city,
            'Компания: ' + obj.company.name,
            'Бизнес: ' + ', '.join([business.name for business in obj.company.business_type.all()]),
            'E-mail: ' + obj.email,
            'Телефон: ' + obj.phone,
            'https://fortisbeauty.store' + url,
        ]
        send_telegeram(msg)


    def send_activation(self):
        user = self.object
        mail_subject = 'Активируйте Вашу учетныую запись FortisBeuty.'
    
        html = render_to_string('user/email/acc_activation_email.html', context={
                'user': user,
                'domain': self.request.META['HTTP_HOST'],
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }, 
        )
        email = EmailMessage(
            mail_subject,
            html,
            'office.fortisbeauty@gmail.com',
            [user.email],
            headers={
                'Reply-To': 'office.fortisbeauty@gmail.com'
            }
        )
        email.content_subtype = "html"
        email.send()


    def get_context_data(self, **kwargs):
        context = super(PartnerRegistration, self).get_context_data(**kwargs)
        context['business__formset'] = BusinessUserFormSetFactory(prefix='business__formset')
        return context


    def get(self, request):
        if request.user.is_authenticated:
            return redirect('user:profile')
        return render(request, self.template_name, {
            'form': self.form,
            'business__formset' : BusinessUserFormSetFactory(prefix='business__formset')
        })


    def form_valid(self, form):
        result = super(PartnerRegistration, self).form_valid(form)
        business_formset = BusinessUserFormSetFactory(form.data, instance=self.object, prefix='business__formset')
        if business_formset.is_valid():
            business_formset.save()
        self.send_activation()
        self.send_to_telegram()
        return result
  

# http://127.0.0.1:8000/activate/MTQ/ap81n2-34d9fb345fec365f1bfac995cde22a12/

def activate(request, uidb64, token):

   
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
        user.is_active = True
        user.save()
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect(reverse('shop:home'))
    else:
        return redirect(reverse('shop:home'))