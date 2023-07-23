from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('add', views.add, name='add'),
    path('add_employee', views.add_employee, name='add_employee'),
    path('add_department', views.add_department, name='add_department'),
    path('add_role', views.add_role, name='add_role'),
    path('view_employees', views.view_employees, name='view_employees'),
    path('view_departments', views.view_departments, name='view_departments'),
    path('view_roles', views.view_roles, name='view_roles'),
    path('view_budgets', views.view_budgets, name='view_budgets'),
    path('employee/<int:pk>', views.employee, name='employee'),
    # path('update_employee/<int:pk>', views.update_employee, name='update_employee'),
    path('delete_employee/<int:pk>', views.delete_employee, name='delete_employee'),
    path('department/<int:pk>', views.department, name='department'),
    path('update_department/<int:pk>', views.update_department, name='update_department'),
    path('delete_department/<int:pk>', views.delete_department, name='delete_department'),
    # path('role/<int:pk>', views.role, name='role'),
    # path('update_role/<int:pk>', views.update_role, name='update_role'),
    # path('delete_role/<int:pk>', views.delete_role, name='delete_role'),
    path('logout', views.logout_user, name='logout')
]