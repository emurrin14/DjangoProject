from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import localtime
from .models import Product, Category, Sale, ProductVariant
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .forms import CustomLoginForm, CustomUserCreationForm
import json


# Create your views here.
def index(request):
    new_products = Product.objects.filter(tags__name__iexact="New").distinct()
    denim_products = Product.objects.filter(tags__name__iexact="Denim").distinct()
    shirt_products = Product.objects.filter(tags__name__iexact="Shirts").distinct()
    jacket_products = Product.objects.filter(tags__name__iexact="Jackets").distinct()

    sale = (
        Sale.objects.filter(is_active=True)
        .order_by('-start_date')
        .first()
    )
    sale_start_iso = sale_end_iso = None

    if sale and sale.start_date:
        sale_start_iso = localtime(sale.start_date).isoformat()
    if sale and sale.end_date:
        sale_end_iso = localtime(sale.end_date).isoformat()
        
    context = {
        'new_products': new_products,
        'denim_products': denim_products,
        'shirt_products': shirt_products,
        'jacket_products': jacket_products,
        'sale': sale,
        'sale_start_iso': sale_start_iso,
        'sale_end_iso': sale_end_iso,
    }
    return render(request, 'index.html', context)

def product(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related('images', 'variants__size', 'variants__color'), 
        slug=slug
    )
    sale = (
        Sale.objects.filter(is_active=True)
        .order_by('-start_date')
        .first()
    )
    sale_start_iso = sale_end_iso = None
    if sale and sale.start_date:
        sale_start_iso = localtime(sale.start_date).isoformat()
    if sale and sale.end_date:
        sale_end_iso = localtime(sale.end_date).isoformat()

    context = {
        'product': product,
        'sale': sale,
        'sale_start_iso': sale_start_iso,
        'sale_end_iso': sale_end_iso,
    }
    return render(request, 'product.html', context)

def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        variant_id = data.get('variant_id')
        quantity = data.get('quantity', 1)

        try:
            variant = ProductVariant.objects.get(id=variant_id)
            #add to cart logic
            return JsonResponse({'success': True, 'message': f'{variant.size} Added To Cart!'})
        except ProductVariant.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Variant not found'}, status=404)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)



def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
    else:
        form = CustomLoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("index")