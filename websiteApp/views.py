from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime
from .models import Product, Category, Sale

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