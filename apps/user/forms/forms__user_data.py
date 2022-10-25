from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms import modelformset_factory
from django.forms import BaseFormSet
from django.forms.widgets import DateInput
from django.forms.models import BaseInlineFormSet
from apps.user.models import CustomUser, UserAdress, UserAdressChosen, UserCompany
from apps.shop.models import Categories
from django.forms.models import inlineformset_factory






class UserDataMainForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name','last_name','father_name','phone','country','city'
        ]

    def __init__(self, *args, **kwargs):
        super(UserDataMainForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')

        for name, field in self.fields.items():
            field.widget.attrs['id'] = f'user_data_main_{name}'
            field.widget.attrs['data-value'] = ''
            
            if getattr(instance, name) in [None,'']:
                field.widget.attrs['placeholder'] = '-'



class UserDataConstactsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'phone','email'
        ]

    def __init__(self, *args, **kwargs):
        super(UserDataConstactsForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        
        for name, field in self.fields.items():
            field.widget.attrs['id'] = f'user_data_contacts_{name}'
            field.widget.attrs['data-value'] = ''
            if getattr(instance, name) in [None,'']:
                field.widget.attrs['placeholder'] = '-'





# ADRESS CHOSEN
class UserAdressChosenFormSet(BaseInlineFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['parent_object'] = self.instance
        return kwargs



class UserAdressChosenForm(forms.ModelForm):
    class Meta:
        model = UserAdressChosen
        fields = [
            'adress'
        ]

    def __init__(self, parent_object, *args, **kwargs):
        super(UserAdressChosenForm, self).__init__(*args, **kwargs)
        self.fields['adress'].label = 'Приоритетный адрес'
        self.fields['adress'].queryset =  self.fields['adress'].queryset.filter(parent=parent_object)

      
       

UserAdressChosenFormSetFactory = inlineformset_factory(
    CustomUser, UserAdressChosen, extra=1,
    fields = [
        'adress'
    ],
    formset = UserAdressChosenFormSet,
    form = UserAdressChosenForm
)



# ADRESS FORM
class UserAdressForm(forms.ModelForm):
    class Meta:
        model = UserAdress
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserAdressForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label

UserAdressFromSet = inlineformset_factory(
    CustomUser, UserAdress, extra=1,
    fields = [
        'id','city','street','house','appartment'
    ],
    form = UserAdressForm
)


class UserCompanyForm(forms.ModelForm):
    class Meta:
        model = UserCompany
        fields = [
            'name','code','email','iban','director','adress','business_type'
        ]

    def __init__(self, *args, **kwargs):
        super(UserCompanyForm, self).__init__(*args, **kwargs)
       

UserCompanyFormSet = inlineformset_factory(
    CustomUser, UserCompany, extra=1,
    fields = [
        'name','code','email','iban','director','adress','business_type'
    ],
)


class UserRealPrice(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'real_stock'
        ]

