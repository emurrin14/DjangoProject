from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# Create your views here.
def index(request):
    new_products = Product.objects.filter(tags__name__iexact="New").distinct()
    denim_products = Product.objects.filter(tags__name__iexact="Denim").distinct()
    shirt_products = Product.objects.filter(tags__name__iexact="Shirts").distinct()
    jacket_products = Product.objects.filter(tags__name__iexact="Jackets").distinct()

    context = {
        'new_products': new_products,
        'denim_products': denim_products,
        'shirt_products': shirt_products,
        'jacket_products': jacket_products,
    }
    return render(request, 'index.html', context)