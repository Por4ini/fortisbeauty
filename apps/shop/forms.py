from django import forms
from apps.shop.models import Comment, Reply

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'user','type','product','rate','text','advantages','disadvantages'
        ]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.fields['type'].widget =    forms.HiddenInput()
        self.fields['user'].widget =    forms.HiddenInput()
        self.fields['product'].widget = forms.HiddenInput()

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'user','type','product','text'
        ]

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        self.fields['type'].widget =    forms.HiddenInput()
        self.fields['user'].widget =    forms.HiddenInput()
        self.fields['product'].widget = forms.HiddenInput()
        self.fields['text'].label = "Вопрос"


    
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = [
            'parent','comment','user','text'
        ]

    def __init__(self, *args, **kwargs):
        super(ReplyForm, self).__init__(*args, **kwargs)

        self.fields['parent'].widget = forms.HiddenInput()
        self.fields['comment'].widget = forms.HiddenInput()
        self.fields['user'].widget =   forms.HiddenInput()



class PromoCodeForm(forms.Form):
    code = forms.CharField(label='Промокод', max_length=20, required=False)
