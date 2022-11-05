from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.urls import reverse
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve


urlpatterns = []

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
  


urlpatterns += i18n_patterns(
    path('',          include('apps.user.urls',      namespace='user')),
    path('blog/',     include('apps.blog.urls',      namespace='blog')),
    path('order/',    include('apps.order.urls',     namespace='order')),
    path('core/',     include('apps.core.urls',      namespace='core')),
    path('search/',   include('apps.search.urls',    namespace='search')),
    path('wishlist/', include('apps.wishlist.urls',  namespace='wishlist')),
    path('opt/',      include('apps.opt.urls',       namespace='opt')),
    path('i18n/',     include('django.conf.urls.i18n')),
    path('admin/clearcache/', include('clearcache.urls')),
    path('admin/',  admin.site.urls),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    
    # path('jet/',    include('jet.urls', 'jet')),
    # path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('1c/',     include('apps.sync1c.urls',  namespace='sync1c')),
    path('',        include('apps.shop.urls',   namespace='shop')),
    path('',        include('apps.pages.urls',  namespace='pages')),
    prefix_default_language=False
)


