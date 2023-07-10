from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add', views.add, name='add'),
    path('view', views.view, name='view'),
    path('add_employee', views.add_employee, name='add_employee'),
    path('add_department', views.add_department, name='add_department'),
    path('add_role', views.add_role, name='add_role'),
]