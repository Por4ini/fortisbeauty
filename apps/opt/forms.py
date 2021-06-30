from django import forms
from django.utils.translation import ugettext_lazy as _
from apps.user.models import CustomUser


class WhoosaleForm(forms.ModelForm):
    want_be_whoosaler = forms.BooleanField(widget=forms.HiddenInput()) 

    class Meta:
        model = CustomUser
        fields = [
            'want_be_whoosaler'
        ]

    def __init__(self,*args, **kwargs):
        super(WhoosaleForm, self).__init__(*args, **kwargs)
    
       
  