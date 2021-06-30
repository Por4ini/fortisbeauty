from django.db import models
from django.forms import TextInput, Textarea


# GLOBALS
FORMFIELD_OVERRIDES = {
    models.CharField: {'widget': TextInput(attrs={'size':'63'})},
    models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':61})},
}
