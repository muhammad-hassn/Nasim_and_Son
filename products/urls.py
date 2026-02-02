from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_landing, name='landing'),
    path('<slug:slug>/', views.product_resolver, name='resolver'),
]
