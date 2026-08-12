from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .models import Category, Product, Cart, CartItem, Rating, Order, OrderItem
from django.contrib import messages
from .forms import RegistrationForm
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('')
        else:
            messages.error(request, 'Invalid username or password')

    return redirect(request, '')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration Successful!')




def logout_view(request):
    logout(request)
    return redirect('')