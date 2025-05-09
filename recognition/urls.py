from django.urls import path
from . import views

urlpatterns = [
    path('', views.recognize_view, name='upload_view'),
]
