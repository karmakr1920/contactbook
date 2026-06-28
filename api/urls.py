from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('contacts/', views.contact_list, name='contact_list_create'),
    path('contacts/<int:pk>/', views.contact_detail,name='contact_detail_update_delete'),
]