from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# Create your views here.
def index(request):
    new_products = Product.objects.filter(new=True)
    return render(request, 'index.html', {'new_products': new_products})