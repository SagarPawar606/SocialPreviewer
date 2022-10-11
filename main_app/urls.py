from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('api/', views.social_api, name='api'),
    path('download-meta/', views.download_meta, name='download_meta'),
]