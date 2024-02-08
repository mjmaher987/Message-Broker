from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main import views

urlpatterns = [
    path('message/', views.message, name='message'),
    path('push/', views.push, name='push'),
    path('pull/', views.pull, name='pull'),
]