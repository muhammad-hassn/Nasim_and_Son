from django.urls import path
from . import views

app_name = 'inquiries'

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_quote, name='add_to_quote'),
    path('update/<int:product_id>/<str:action>/', views.update_quote, name='update_quote'),
    path('remove/<int:product_id>/', views.remove_from_quote, name='remove_from_quote'),
    path('quote/', views.quote_list, name='quote_list'),
]
