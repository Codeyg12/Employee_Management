from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import RegisterForm, AddDepartmentForm, AddRoleForm, AddEmployeeForm
from .models import Employee, Role, Department
from django.http import JsonResponse
from django.urls import reverse

model_map = {
    "employee": {"name": Employee, "form": AddEmployeeForm},
    "role": {"name": Role, "form": AddRoleForm},
    "department": {"name": Department, "form": AddDepartmentForm},
}

loginNeeded = "You must be logged in.."


# Create your views here.
def home(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Log in successful")
            return redirect("home")
        else:
            messages.error(request, "There was an error logging in")
            return redirect("home")

    else:
        return render(request, "home.html", {})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully register")
            return redirect("home")
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})

    return render(request, "register.html", {"form": form})


def add(request, name):
    form = model_map[name]["form"](request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                update_url = reverse("view", kwargs={"name": name})
                messages.success(request, f"New {name.capitalize()} Added")
                return redirect(update_url)
        return render(request, "add.html", {"form": form, "name": name})
    else:
        messages.error(request, loginNeeded)
        return redirect("home")


def view(request, name):
    if request.user.is_authenticated:
        all = model_map[name]["name"].objects.all()
        per_page = 8
        paginator = Paginator(all, per_page)
        page = request.GET.get("page")
        add_url = reverse("add", kwargs={'name': name})

        try:
            current = paginator.page(page)
        except PageNotAnInteger:
            current = paginator.page(1)
        except EmptyPage:
            current = paginator.page(paginator.num_pages)
        return render(request, f"view_{name}s.html", {"current": current, 'add_url': add_url, 'name': name})
    else:
        messages.error(request, loginNeeded)
        return redirect("home")


def view_budgets(request):
    if request.user.is_authenticated:
        options = Department.objects.all()
        return render(request, "view_budgets.html", {"options": options})
    else:
        messages.error(request, loginNeeded)
        return redirect("home")

def update(request, name, pk):
    if request.user.is_authenticated:
        current = model_map[name]["name"].objects.get(id=pk)
        form = model_map[name]["form"](request.POST or None, instance=current)
        if form.is_valid():
            form.save()
            update_url = reverse("view", kwargs={"name": name})
            messages.success(request, f"{name.capitalize()} updated")
            return redirect(update_url)
        return render(
            request, "update.html", {"form": form, "current": current, "name": name}
        )
    else:
        messages.error(request, loginNeeded)
        return redirect("home")

def delete_record(request, name, pk):
    if request.user.is_authenticated:
        delete_record = model_map[name]["name"].objects.get(id=pk)
        delete_record.delete()
        update_url = reverse("view", kwargs={"name": name})
        messages.success(request, f"{name.capitalize()} successfully deleted")
        return redirect(update_url)
    else:
        messages.error(request, loginNeeded)
        return redirect("home")
    
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home")

def employee(request, pk):
    if request.user.is_authenticated:
        single_employee = Employee.objects.get(id=pk)
        delete_url = reverse(
            "delete_record", kwargs={"name": "employee", "pk": single_employee.id}
        )
        return render(
            request,
            "employee.html",
            {"single_employee": single_employee, "delete_url": delete_url},
        )
    else:
        messages.error(request, loginNeeded)
        return redirect("home")

def department(request, pk):
    if request.user.is_authenticated:
        single_department = Department.objects.get(id=pk)
        delete_url = reverse(
            "delete_record", kwargs={"name": "department", "pk": single_department.id}
        )
        employees = Employee.objects.filter(employee_department=single_department)
        total = 0
        for employee in employees:
            total += employee.employee_role.salary
        return render(
            request,
            "department.html",
            {
                "single_department": single_department,
                "employees": employees,
                "total": total,
                "delete_url": delete_url,
            },
        )
    else:
        messages.error(request, loginNeeded)
        return redirect("home")

def role(request, pk):
    if request.user.is_authenticated:
        single_role = Role.objects.get(id=pk)
        delete_url = reverse(
            "delete_record", kwargs={"name": "role", "pk": single_role.id}
        )
        return render(
            request, "role.html", {"single_role": single_role, "delete_url": delete_url}
        )
    else:
        messages.error(request, loginNeeded)
        return redirect("home")


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
                roles[position]["total_salary"] += salary
                roles[position]["count"] += 1
            else:
                roles[position] = {"count": 1, "total_salary": salary}

            # context = {'department': department, 'total': total, 'roles': roles, 'employees': employees}
            # plug context into render?

        return render(
            request,
            "budget.html",
            {
                "department": department,
                "total": total,
                "roles": roles,
                "employees": employees,
            },
        )
    else:
        messages.error(request, loginNeeded)
        return redirect("home")

def get_department_by_role(request):
    if request.method == "GET" and "role_id" in request.GET:
        role_id = request.GET["role_id"]
        try:
            role = Role.objects.get(id=role_id)
            department_id = role.role_department.id
            return JsonResponse({"department_id": department_id})
        except Role.DoesNotExist:
            return JsonResponse({"error": "Role not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


def custom_404(request, exception):
    return render(request, "custom_404.html", status=404)


def custom_500(request, exception=None):
    return render(request, "custom_500.html", status=500)
