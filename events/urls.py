# urls.py
from django.urls import path
from .views import event_list, event_create

app_name = 'events'
urlpatterns = [
    path('', event_list, name='event_list'),
    path('add/', event_create, name='event_create'),
]
