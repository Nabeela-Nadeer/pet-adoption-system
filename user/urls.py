from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # root URL
    path('register/', views.register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('request-adoption/<int:pet_id>/', views.request_adoption, name='request_adoption'),
    path('cancel-adoption/<int:pet_id>/', views.cancel_adoption, name='cancel_adoption'),
    path('adoption-history/', views.adoption_history, name='adoption_history'),
    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'),
]
