from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('add/<str:name>', views.add, name='add'),
    path('view/<str:name>', views.view, name='view'),
    path('update/<str:name>/<int:pk>/', views.update, name='update'),
    path('delete_record/<str:name>/<int:pk>', views.delete_record, name='delete_record'),
    path('employee/<int:pk>', views.employee, name='employee'),
    path('department/<int:pk>', views.department, name='department'),
    path('role/<int:pk>', views.role, name='role'),
    path('get_department_by_role', views.get_department_by_role, name='get_department_by_role'),
    path('logout', views.logout_user, name='logout')
]