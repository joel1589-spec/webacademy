from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls')),
    path('comptes/', include('comptes.urls')),
    path('verification/', include('attestations.urls')),
    path('ressources/', include('ressources.urls')),
    path('services/', include('services.urls')),
    path('annonces/', include('annonces.urls')),
    path('blog/', include('blog.urls')),
    path('messagerie/', include('messagerie.urls')),
    path('assistant/', include('assistant.urls')),
    path('examens/', include('examens.urls')),
]

if settings.DEBUG and not settings.USE_CLOUDINARY:
    # En local sans Cloudinary configuré : on sert les médias depuis le
    # disque, comme avant. En production (ou dès que Cloudinary est
    # configuré), les fichiers sont hébergés et servis par Cloudinary lui-même
    # via son CDN — inutile que Django s'en charge.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Web Academy — Administration"
admin.site.site_title = "Web Academy Admin"
admin.site.index_title = "Gestion du site (attestations, ressources, annonces, blog, services, apprenants)"
