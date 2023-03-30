from django.urls import include, path, re_path
from apps.order import views
from django.views.generic import TemplateView

app_name = 'orders'


urlpatterns = [
   path('', views.OrderViewSet.as_view({'get':'data'}), name='order'),
   re_path(
      r"^(?P<delivery>newpost|curier)/",
      views.OrderViewSet.as_view({'get':'data', 'post':'data'}), 
      name='order'
   ),
   re_path(
      r"^api/(?P<delivery>newpost|curier)/",
      views.OrderViewSet.as_view({'post':'api'}), 
      name='order_api'
   ),
   path('create/',          views.CreateOrderView.as_view(), name='create'),
   path('payment/',         views.OrderPay.as_view(),    name='payment'),
   path('prepayment/',      views.OrderPrePay.as_view(),    name='prepayment'),
   path('repeat/<id>/',     views.OrderRepeat.as_view(), name="repeat"),
   path('success/',         views.order_success,         name='success'),
   path('payment_response', views.payment_response,      name="payment_response"),
   path('apply_promo', views.views__promocode.apply_promo, name="apply_promo"),

]
