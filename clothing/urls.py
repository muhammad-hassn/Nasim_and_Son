from django.urls import path
from . import views

app_name = 'clothing'

urlpatterns = [
    path('', views.clothing_list, name='list'),
    path('category/<slug:category_slug>/', views.clothing_list, name='category_detail'),
    path('product/<slug:slug>/', views.clothing_detail, name='product_detail'),
]
