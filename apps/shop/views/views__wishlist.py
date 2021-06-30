from rest_framework import viewsets



class WishlistView(viewsets.ViewSet):
    def get(request):
        print('wishlist')
        return Response({})