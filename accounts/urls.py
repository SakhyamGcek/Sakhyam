from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('registration_complete/', views.registration_complete, name='registration_complete'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('approve_user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('disapprove_user/<int:user_id>/', views.disapprove_user, name='disapprove_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user_landing_page/', views.user_landing_page, name='user_landing_page'),
    path('set_password/', views.set_password, name='set_password'),
    path('set_password/<uidb64>/<token>/', views.set_initial_password, name='set_initial_password'),
    
    path('password_set_complete/', views.password_set_complete, name='password_set_complete'),
]
