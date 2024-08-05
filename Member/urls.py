from django.urls import path
from . import views

app_name ='member'
urlpatterns = [
    path('member_list/', views.member_list, name='member_list'),
    path('member_create/', views.member_create , name='member_create'),
    #path('member_requests/', views.member_requests, name='member_requests'),
    path('approve_member/<int:member_id>/', views.approve_member, name='approve_member'),
    path('assign_role/<int:member_id>/', views.assign_role, name='assign_role'),
    path('delete/<int:member_id>/', views.delete_member, name='delete_member'),
]
