from django.contrib import admin
from django.urls import path,include
#for media url
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('meriemecomsite/', admin.site.urls),
    path('',include('store.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
