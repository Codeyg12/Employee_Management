from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def add(request):
    return render(request, 'add.html', {})

def view(request):
    return render(request, 'view.html', {})