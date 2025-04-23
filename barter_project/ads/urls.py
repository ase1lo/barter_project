from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_ad, name='create_ad'),
    path('success/', views.ad_success, name='ad_success')
]