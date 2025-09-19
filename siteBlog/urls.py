from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webapp.urls')),
]

# ✅ Static files (Whitenoise handle karega)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ✅ Media files (Cloudinary handle karega automatically, 
# optional to include for templates using MEDIA_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webapp.urls')),
]

# ✅ Static files (Whitenoise handle karega)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ✅ Media files (Cloudinary handle karega automatically, 
# optional to include for templates using MEDIA_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
