from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('netscanner', views.network_scanner, name='network_scanner'),
    path('portscanner', views.port_scanner, name='port_scanner'),
    path('webfuzzer', views.web_fuzzer, name='web_fuzzer'),
]