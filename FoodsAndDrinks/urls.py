from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('foods/', include('foods.urls')),
    path('comments/', include('comments.urls')),
    path('cart/', include('cart.urls')),
    path('', include('users.urls')),
]

if settings.DEBUG is True:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

