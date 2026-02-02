from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('company/', views.company, name='company'),
    path('contact-us/', views.contact, name='contact'),
]
