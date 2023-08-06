from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum
from .forms import RegisterForm, AddDepartmentForm, AddRoleForm, AddEmployeeForm
from .models import Employee, Role, Department

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

def add(request):
    return render(request, 'add.html', {})

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
    employees = Employee.objects.all()
    return render(request, 'view_employees.html', {'employees':employees})

def view_departments(request):
    departments = Department.objects.all()
    return render(request, 'view_departments.html', {'departments':departments})

def view_roles(request):
    roles = Role.objects.all()
    return render(request, 'view_roles.html', {'roles':roles})

def view_budgets(request):
    options = Department.objects.all()
    return render(request, 'view_budgets.html', {'options': options})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

def employee(request, pk):
    single_employee = Employee.objects.get(id=pk)
    return render(request, 'employee.html', {'single_employee': single_employee})

def delete_employee(request, pk):
    delete_record = Employee.objects.get(id=pk)
    delete_record.delete()
    messages.success(request, 'Employee record deleted')
    return redirect('view_employees')

def department(request, pk):
    single_department = Department.objects.get(id=pk)
    return render(request, 'department.html', {'single_department': single_department})

def delete_department(request, pk):
    if request.user.is_authenticated:
        delete_record = Department.objects.get(id=pk)
        delete_record.delete()
        messages.success(request, 'Department successfully deleted')
        return redirect('view_departments')
    else:
        messages.error(request, 'You need to be logged in')
        return redirect('home')

def update_department(request, pk):
    if request.user.is_authenticated:
        current_department = Department.objects.get(id=pk)
        form = AddDepartmentForm(request.POST or None, instance=current_department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated')
            return redirect('view_departments')
        return render(request, 'update_department.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')
    
def role(request, pk):
    single_role = Role.objects.get(id=pk)
    return render(request, 'role.html', {'single_role': single_role})

def delete_role(request, pk):
    if request.user.is_authenticated:
        delete_role = Role.objects.get(id=pk)
        delete_role.delete()
        messages.success(request, 'Role has been deleted')
        return redirect('view_roles')
    else:
        messages.error(request, 'You need to be logged in')
        return redirect('home')
    
def update_role(request, pk):
    if request.user.is_authenticated:
        current_role = Role.objects.get(id=pk)
        form = AddRoleForm(request.POST or None, instance=current_role)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role updated')
            return redirect('view_roles')
        return render(request, 'update_role.html', {'form': form})
    else:
        messages.error(request, 'You need to be logged in')
        return redirect('home')
    
def update_employee(request, pk):
    if request.user.is_authenticated:
        current_employee = Employee.objects.get(id=pk)
        form = AddEmployeeForm(request.POST or None, instance=current_employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated')
            return redirect('view_employees')
        return render(request, 'update_employee.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')

def budget(request, pk):
    if request.user.is_authenticated:
        department = Department.objects.get(id=pk)
        employees = Employee.objects.filter(employee_department=department)
        all_roles = Role.objects.filter(role_department=department)
        print(f'ALL {all_roles}')
        roles = []
        # for role in all_roles:
        #     single_role = {'title': role.title, 'salary': role.salary}
        #     print(single_role)
        #     roles.append(single_role)

        total = 0
        for employee in employees:
            roles.append(employee.employee_role)
            total += employee.employee_role.salary
        for role in roles:
            print(role, role.salary)
        print(roles)
        return render(request, 'budget.html', {'department': department, 'total': total, 'roles': roles})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')
    
