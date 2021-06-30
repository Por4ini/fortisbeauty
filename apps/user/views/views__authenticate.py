from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from apps.user.forms import LoginForm
from django.views import View



class LoginView(View):
    form_class = LoginForm
    template_name = 'user/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('user:profile')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('user:profile')
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                if request.META.get('HTTP_REFERER'):
                    return redirect(request.META.get('HTTP_REFERER'))
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                if request.GET.get('redirect'):
                    return redirect(request.GET.get('redirect'))
                return redirect('/')
        return render(request, self.template_name, {'form': form})



def user_logout(request):
    logout(request)
    return redirect('/')









