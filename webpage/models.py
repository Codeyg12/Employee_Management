from django.db import models

# Create your models here.
class Department(models.Model):
    department_name = models.CharField(max_length=50)

    def __str__(self):
        return(f'{self.department_name}')

class Role(models.Model):
    title = models.CharField(max_length=50)
    salary = models.IntegerField()
    role_department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return(f'{self.title}')

class Employee(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    employee_role = models.ForeignKey(Role, on_delete=models.CASCADE)
    employee_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    manager = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return(f'{self.first_name} {self.last_name}')