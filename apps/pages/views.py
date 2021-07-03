from django.shortcuts import render
from django.utils import translation
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from apps.pages.models import (
    Page,
    PageContacts,
    PageAbout,
    PagePayment,
    PageDelivery,
    PageTermsOfUse
)
from apps.main.forms import MessagesForm
from apps.core.functions import send_telegeram



class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/page.html'
    context_object_name = 'page'



def page_about(request):
    return render(request, 'pages/page.html', {
        'page' : PageAbout.objects.first(),
    })


def page_payment(request):
    return render(request, 'pages/page.html', {
        'page' : PagePayment.objects.first(),
    })


def page_delivery(request):
    return render(request, 'pages/page.html', {
        'page' : PageDelivery.objects.first(),
    })


def page_terms_of_use(request):
    return render(request, 'pages/page.html', {
        'page' : PageTermsOfUse.objects.first(),
    })




class ContactFormView(FormView):
    template_name = 'pages/page__contacts.html'
    form_class = MessagesForm
    success_url = '/contacts/successs/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = PageContacts.objects.first()
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.save()

            msg = []

            translation = {
                'subject' : 'Тема',
                'first_name' : 'Имя',
                'email' : 'E-mail',
                'phone' : 'Телфон',
                'text' : 'Сообьщение',
            }
        
            for k, v in form.cleaned_data.items():
                msg.append(translation[k] + ': ' + v)

            send_telegeram(msg)

        return super().form_valid(form)



# def page_constacts(request):
#     form_valid = False
#     if request.method == 'POST':
#         form = MessagesForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             form_valid = True
#     else:
#         data = {}
#         if request.user.is_authenticated:
#             user = request.user
#             data = model_to_dict(user)
#         form = MessagesForm(initial=data)

#     print(form)
#     return render(request, 'pages/page__contacts.html', {
#         'page' : PageContacts.objects.first(),
#         'form' : form, 
#         'form_valid' : form_valid,
#     })