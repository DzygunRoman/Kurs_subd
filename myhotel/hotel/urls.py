from django.urls import path, re_path, register_converter
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='home'),  # http://127.0.0.1:8000
    path('add_client/', views.add_client, name='add_client'),
    path('duty_schedule/', views.duty_schedule, name='duty_schedule'),
    path('service_room/', views.service_room, name='service_room'),
    path('number_distribution/', views.number_distribution, name='number_distribution'),
    path('redactor_number/', views.redactor_number, name='redactor_number'),
    path('redactor_category/', views.redactor_category, name='redactor_category'),
]