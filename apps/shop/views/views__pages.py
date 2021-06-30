from django.shortcuts import render


def about(request):
    args={}
    return render(request, 'shop/shop__about.html', args)


def delivery(request):
    args={}
    return render(request, 'shop/shop__delivery.html', args)


def guarantee(request):
    args={}
    return render(request, 'shop/shop__guarantee.html', args)


def contacts(request):
    args = {}
    return render(request, 'shop/public-offer.html', args)


def public_offer(request):
    args = {}
    return render(request, 'shop/public-offer.html', args)