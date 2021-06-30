from django.contrib.auth import views as auth_views
from apps.user.forms import PasswordRestoreForm


class RestorePasswordFormView(auth_views.PasswordResetView):
    form_class = PasswordRestoreForm
    from_email = 'office.fortisbeauty@gmail.com'
    template_name = 'user/password_restore/form.html'
    email_template_name = 'user/password_restore/email_template.html',
    html_email_template_name = 'user/password_restore/email_template.html',
    success_url = '/restore_password/success/'