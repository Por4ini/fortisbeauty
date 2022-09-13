from django.views.generic.edit import UpdateView
from django.utils.encoding import force_text
from django.urls import reverse
from apps.user.models import CustomUser
from apps.opt.models import WhoosaleText
from apps.opt.forms import WhoosaleForm
from apps.core.functions import send_telegeram



class WhoosaleView(UpdateView):
    model = CustomUser
    success_url =   '/opt/success'
    template_name = 'opt/opt.html'
    form_class = WhoosaleForm

    def get_object(self):
        if self.request.user:
            return self.request.user
        return None

    def get_initial(self):
        initial = super().get_initial()
        initial['want_be_whoosaler'] = True
        return initial
    
    def get_context_data(self, **kwargs):
        context = {}
        if self.request.user.is_authenticated:
            context = super(WhoosaleView, self).get_context_data(**kwargs)
        context['text'] = WhoosaleText.objects.last()
        return context

    def send_to_telegram(self):
        obj = self.request.user
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
        msg = [
            'Зарегестриованный пользовател хочет продавать оптом.' + '\n'
            'url:' + 'https://fortisbeauty.store' + url
        ]
        send_telegeram(msg)

    

    def form_valid(self, form):
        result = super(WhoosaleView, self).form_valid(form)
        self.send_to_telegram()
        return result



 