from django.urls import path
from .views import request_view

urlpatterns = [
    path('request', request_view, name='request-api'),
]