from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('checkin/', views.check_in, name='check_in'),
    path('checkout/', views.check_out, name='check_out'),
    path('attendance-history/', views.attendance_history, name='attendance_history'),
]