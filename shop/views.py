from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .models import Category, Product, Cart, CartItem, Rating, Order, OrderItem
from django.contrib import messages
from .forms import RegistrationForm
from django.db.models import Q, Min, Max, Avg
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('shop:register')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'shop/login.html')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration Successful!')
            return redirect('shop:login')
    else:
        form = RegistrationForm() 
    return render(request, 'shop/register.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('shop:login')


def home(request):
    featured_products = Product.objects.filter(available=True).order_by('-created-at')[:8]
    categories = Category.objects.all()

    return render(request, '', {
        'featured_products': featured_products,
        'categories': categories
    })

