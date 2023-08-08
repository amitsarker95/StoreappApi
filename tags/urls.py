from django.urls import path
from .views import query


urlpatterns = [
    path('rel/', query, name='query'),
]