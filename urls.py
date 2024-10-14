from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import custom_logout, available_residences, select_residences


urlpatterns = [
    path('student_register/', views.student_register, name='student_register'),
    path('home/', views.home, name='home'),
    path('student_login/', views.student_login, name='student_login'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student_details/', views.student_details, name='student_details'),
    path('success/', views.success, name='success'),
    path('logout/', custom_logout, name='logout'), 
    path('admin_dashboard/', views.admin_dashboard , name='admin_dashboard'),
    path('available-residences/', available_residences, name='available_residences'),
    path('select_residences/', select_residences, name='select_residences'),

]
