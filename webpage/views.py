from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import Counter
from .forms import RegisterForm, AddDepartmentForm, AddRoleForm, AddEmployeeForm
from .models import Employee, Role, Department
import random
from django.http import JsonResponse

# Create your views here.
def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Log in successful')
            return redirect('home')
        else:
            messages.error(request, 'There was an error logging in')
            return redirect('home')
        
    else:
        return render(request, 'home.html', {})
    
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully register')
            return redirect('home')
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})

def add_employee(request):
    form = AddEmployeeForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'New Employee Added')
                return redirect('view_employees')
        return render(request, 'add_employee.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')

def add_department(request):
    form = AddDepartmentForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'New Department Added')
                return redirect('view_departments')
        return render(request, 'add_department.html', {'form':form})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')  

def add_role(request):
    form = AddRoleForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'New Role Added')
                return redirect('view_roles')
        return render(request, 'add_role.html', {'form':form})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')

def view_employees(request):
    if request.user.is_authenticated:
        all_employees = Employee.objects.all()
        # random_employees = Employee.objects.all().order_by('?')
        employees_per_page = 10
        paginator = Paginator(all_employees, employees_per_page)
        page = request.GET.get('page')

        try: 
            employees = paginator.page(page)
        except PageNotAnInteger:
            employees = paginator.page(1)
        except EmptyPage:
            employees = paginator.page(paginator.num_pages)
        return render(request, 'view_employees.html', {'employees':employees})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')

def view_departments(request):
    if request.user.is_authenticated:
        departments = Department.objects.all()
        return render(request, 'view_departments.html', {'departments':departments})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')

def view_roles(request):
    if request.user.is_authenticated:
        roles = Role.objects.all()
        return render(request, 'view_roles.html', {'roles':roles})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')

def view_budgets(request):
    if request.user.is_authenticated:
        options = Department.objects.all()
        return render(request, 'view_budgets.html', {'options': options})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

def employee(request, pk):
    if request.user.is_authenticated:
        single_employee = Employee.objects.get(id=pk)
        return render(request, 'employee.html', {'single_employee': single_employee})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')

def delete_employee(request, pk):
    if request.user.is_authenticated:
        delete_record = Employee.objects.get(id=pk)
        delete_record.delete()
        messages.success(request, 'Employee record deleted')
        return redirect('view_employees')
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')
    
def department(request, pk):
    if request.user.is_authenticated:
        single_department = Department.objects.get(id=pk)
        employees = Employee.objects.filter(employee_department=single_department)
        total = 0

        for employee in employees:
            total += employee.employee_role.salary
        return render(request, 'department.html', {'single_department': single_department, 'employees': employees, 'total': total})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')
    
def delete_department(request, pk):
    if request.user.is_authenticated:
        delete_record = Department.objects.get(id=pk)
        delete_record.delete()
        messages.success(request, 'Department successfully deleted')
        return redirect('view_departments')
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')

def update(request, name, pk):
    if request.user.is_authenticated:
        update_map = {
            'employee': {
                'name': Employee,
                'form': AddEmployeeForm
                },
            'role': {
                'name': Role,
                'form': AddRoleForm
                },
            'department': {
                'name': Department,
                'form': AddDepartmentForm
                },
            }
        current = update_map[name]['name'].objects.get(id=pk)
        form = update_map[name]['form'](request.POST or None, instance=current)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated')
            return redirect('view_departments')
        return render(request, 'update.html', {'form': form, 'current': current, 'name': name})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')
    
def role(request, pk):
    if request.user.is_authenticated:
        single_role = Role.objects.get(id=pk)
        return render(request, 'role.html', {'single_role': single_role})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')

def delete_role(request, pk):
    if request.user.is_authenticated:
        delete_role = Role.objects.get(id=pk)
        delete_role.delete()
        messages.success(request, 'Role has been deleted')
        return redirect('view_roles')
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')
    
def budget(request, pk):
    if request.user.is_authenticated:
        department = Department.objects.get(id=pk)
        employees = Employee.objects.filter(employee_department=department)

        roles = {}
        total = 0

        for employee in employees:
            total += employee.employee_role.salary
            position = employee.employee_role
            salary = employee.employee_role.salary

            if position in roles:
                roles[position]['total_salary'] += salary
                roles[position]['count'] += 1
            else:
                roles[position] = {'count': 1, 'total_salary': salary}

            # context = {'department': department, 'total': total, 'roles': roles, 'employees': employees}
            # plug context into render?

        return render(request, 'budget.html', {'department': department, 'total': total, 'roles': roles, 'employees': employees})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')
    
def department_employees(request, pk):
    if request.user.is_authenticated:
        department = Department.objects.get(id=pk)
        employees = Employee.objects.filter(employee_department=department)
        return render(request, 'department_employees.html', {'department': department, 'employees': employees})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')
    
def get_department_by_role(request):
    if request.method == 'GET' and 'role_id' in request.GET:
        role_id = request.GET['role_id']
        try:
            role = Role.objects.get(id=role_id)
            department_id = role.role_department.id
            return JsonResponse({'department_id': department_id})
        except Role.DoesNotExist:
            return JsonResponse({'error': 'Role not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def custom_404(request, exception):
    return render(request, 'custom_404.html', status=404)

def custom_500(request, exception=None):
    return render(request, 'custom_500.html', status=500)