from django.urls import path

from . import views

urlpatterns = [
    path('message/', views.message, name='message'),
    path('push/', views.push, name='push'),
    path('pull/', views.pull, name='pull'),
]