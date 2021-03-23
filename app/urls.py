from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from logistics.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('summernote/', include('django_summernote.urls')),
    path('', HomePageView.as_view(), name="home"),
    path('login/', include('login.urls')),
    path('sale/', include('sale.urls')),
    path('purchase/', include('purchase.urls')),
    path('handbook/', include('handbook.urls')),
    path('logistics/', include('logistics.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
