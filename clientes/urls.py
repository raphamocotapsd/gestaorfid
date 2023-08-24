from django.urls import path

from clientes.views import *

urlpatterns = [
    path('', home),
    path('os/', os, name="form_modelform"),
]
