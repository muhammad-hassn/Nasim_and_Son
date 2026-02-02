from django.urls import path
from . import views

app_name = 'inquiries'

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_quote, name='add_to_quote'),
    path('quote/', views.quote_list, name='quote_list'),
]
