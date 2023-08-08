from django.contrib import admin
from django.urls import path, include
import debug_toolbar

admin.site.site_header = "Store app"
admin.site.index_title = "Admin panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('playground/', include('playground.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('tags/', include('tags.urls')),
    path('store/', include('store.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
