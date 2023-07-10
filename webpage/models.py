from django.db import models

# Create your models here.
# class Department(models.Model):
#     department_name = models.CharField(max_length=50)

# class Role(models.Model):
#     title = models.CharField(max_length=50)
#     salary = models.IntegerField()
#     role_department = models.ForeignKey(Department)

# class Employee(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     employee_role = models.ForeignKey(Role)
#     employee_department = models.ForeignKey(Department)
#     manager = models.ForeignKey('self')