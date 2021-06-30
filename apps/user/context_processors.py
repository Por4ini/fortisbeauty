# from apps.user.models import UserWishlist
from apps.shop.models import Variant

def wishlist(request):
    # if request.user.is_authenticated:
    #     wishlist = UserWishlist.objects.filter(parent=request.user)
    #     for item in wishlist:
    #         print(item.total())
    # else:
    #     wishlist = []
    return {'wishlist' : ''}