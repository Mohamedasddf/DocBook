from django.urls import path 
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('loginform/', views.login_view, name='loginform'),
    path('doctor_detail/<slug:slug>/', views.doctor_detail, name='doctor_detail'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('signup/', views.signup, name='signup'),
    path('updateuser/', views.updateuser, name='updateuser'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    path('logout/', views.logout_view, name='logout'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('appointments/', views.upcoming_appointments, name='upcoming_appointments'),  # عرض المواعيد القادمة
    path('doctor/<slug:slug>/available-times/', views.available_times, name='available_times'),
    path('doctor/<slug:slug>/book/<str:appointment_time>/', views.book_appointment, name='book_appointment'),
    path('appointment/<int:appointment_id>/confirmation/', views.appointment_confirmation, name='appointment_confirmation'),
    path('appointments/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('search/', views.search_doctor, name='search_doctor'),
    path('doctordashboard/', views.doctor_dashboard, name='doctor_dashboard'),

]