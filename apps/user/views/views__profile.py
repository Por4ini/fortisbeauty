from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from apps.user.forms.forms__user_data import *
from apps.order.models import Order
from apps.order.serializers import OrderSerializer
from apps.shop.models import Comment


@login_required()
def user_data(request):
    context = {}
    user=request.user
    forms = {
        'main' :           UserDataMainForm, 
        'contacts' :       UserDataConstactsForm,
        'adress_chosen' :  UserAdressChosenFormSetFactory,
        'adress' :         UserAdressFromSet,
    }

    if request.method == 'POST':
        key = request.GET.get('form')
        if key in forms.keys():
            form = forms[key](data=request.POST, instance=user)
            if form.is_valid():
                form.save()

    for key in forms.keys():
        form = forms[key]
        forms[key] = form(instance=user)
            
    context['forms'] = forms
    return render(request, 'user/profile/profile__userdata.html', context)


@login_required()
def user_orders(request):
    orders = OrderSerializer(
        Order.objects.filter(user=request.user), many=True
    ).data
    return render(request, 'user/profile/profile__orders.html', {'orders' : orders})


@login_required()
def user_wishlist(request):
    return render(request, 'user/profile/profile__wishlist.html')


@login_required()
def user_company(request):
   
    if request.method == 'POST':
        # Company form
        if request.GET.get('real_price'):
            # See real prices
            real_price_form = UserRealPrice(data=request.POST, instance=request.user)
            if real_price_form.is_valid():
                real_price_form.save()
        else:
            formset = UserCompanyFormSet(data=request.POST, instance=request.user)
            if formset.is_valid():
                formset.save()
        
    
    # Company form
    formset = UserCompanyFormSet(instance=request.user)
        # See real prices
    real_price_form = UserRealPrice(instance=request.user)

    return render(request, 'user/profile/profile__company.html', {
        'formset' : formset,
        'real_price_form' : real_price_form

    })


@login_required()
def user_password_change(request):
    done = False
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('user:user_password_change'))
    else:
        form = PasswordChangeForm(user = request.user)
    return render(request, 'user/profile/profile__passwordchange.html', {'form':form, 'done' : done})


@login_required()
def user_logout(request):
    logout(request)
    return redirect('/')


@login_required()
def user_comments(request):
    comments = Comment.objects.filter(user=request.user, type="COMMENT")
    return render(request, 'user/profile/profile__comments.html', {
        'comments': comments
    })

@login_required()
def user_questions(request):
    comments = Comment.objects.filter(user=request.user, type="QUESTION")
    return render(request, 'user/profile/profile__questions.html', {
        'comments': comments
    })