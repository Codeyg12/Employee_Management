from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add', views.add, name='add'),
    path('view', views.view, name='view'),
    path('add_employee', views.add_employee, name='add_employee'),
    path('add_department', views.add_department, name='add_department'),
    path('add_role', views.add_role, name='add_role'),
    path('view_employees', views.view_employees, name='view_employees'),
    path('view_departments', views.view_departments, name='view_departments'),
    path('view_roles', views.view_roles, name='view_roles'),
    path('view_budgets', views.view_budgets, name='view_budgets'),
    path('logout', views.logout_user, name='logout')
]