from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm

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

# def view(request):
#     return render(request, 'view.html', {})

def add_employee(request):
    return render(request, 'add_employee.html', {})

def add_department(request):
    return render(request, 'add_department.html', {})

def add_role(request):
    return render(request, 'add_role.html', {})

def view_employees(request):
    return render(request, 'view_employees.html', {})

def view_departments(request):
    return render(request, 'view_departments.html', {})

def view_roles(request):
    return render(request, 'view_roles.html', {})

def view_budgets(request):
    return render(request, 'view_budgets.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')