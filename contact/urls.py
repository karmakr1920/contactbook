from django.urls import path
from . import views

urlpatterns = [
    
    path('register/', views.register, name='register'),
    path('', views.contact_list, name='contact_list'),
    path('add/', views.add_contact, name='add_contact'),
    path('<int:contact_id>/', views.get_contact, name='get_contact'),
    path('<int:contact_id>/update/', views.update_contact, name='update_contact'),
    path('<int:contact_id>/delete/', views.delete_contact, name='delete_contact'),
]