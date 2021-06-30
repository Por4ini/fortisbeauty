# from django import forms
# from apps.core.models import Message


# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         fields = ['subject','first_name','email','phone','text']

#     def __init__(self, *args, **kwargs):
#         super(MessageForm, self).__init__(*args, **kwargs)
#         # SUBJECT
#         self.fields['subject'].label = ''
#         self.fields['subject'].required = True
#         self.fields['subject'].widget.attrs['data-alert'] =  'Введите тему письма'
#         self.fields['subject'].widget.attrs['placeholder'] = 'Тема письма *'
#         # EMAIL
#         self.fields['email'].label = ''
#         self.fields['email'].required = False
#         self.fields['email'].widget.attrs['data-alert'] =  'Введите Ваш Email'
#         self.fields['email'].widget.attrs['data-error'] =  'Email имеет не верный формат'
#         self.fields['email'].widget.attrs['placeholder'] = 'Email *'
#         # PHONE
#         self.fields['phone'].label = ''
#         self.fields['phone'].required = True
#         self.fields['phone'].widget.attrs['data-alert'] =  'Введите Номер телефона'
#         self.fields['phone'].widget.attrs['placeholder'] = 'Номер телефона'
#         # FIRST NAME
#         self.fields['first_name'].label = ''
#         self.fields['first_name'].required = True
#         self.fields['first_name'].widget.attrs['data-alert'] =  'Ваше имя'
#         self.fields['first_name'].widget.attrs['placeholder'] = 'Ваше имя *'
       
