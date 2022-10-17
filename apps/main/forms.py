from django import forms
from apps.main.models import Message




class MessagesForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject','first_name','email','phone','text']

    def __init__(self, *args, **kwargs):
        super(MessagesForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['id'] = f'conatct_form_{name}'
            field.label=""

        self.fields['subject'].widget.attrs['data-type'] = "text"
        self.fields['first_name'].widget.attrs['data-type'] = "text"
        self.fields['email'].widget.attrs['data-type'] = "email"
        self.fields['phone'].widget.attrs['data-type'] = "text"

