from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('netscanner', views.network_scanner, name='network_scanner'),
]