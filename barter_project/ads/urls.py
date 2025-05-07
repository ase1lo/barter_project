from django.urls import path
from . import views

urlpatterns = [
    path('', views.ads_list, name='ads_list'),
    path('create/', views.create_ad, name='create_ad'),
    path('success/', views.ad_success, name='ad_success'),
    path('ads/<int:ad_id>/edit/', views.update_ad, name='update_ad'),
    path('ads/<int:ad_id>/delete/', views.delete_ad, name='delete_ad'),
    path('proposals/create/', views.create_proposal, name='create_proposal'),
    path('proposals/', views.user_proposals, name='user_proposals'),
]