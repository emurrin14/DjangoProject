from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import localtime
from .models import Product, Category, Sale, ProductVariant, Cart, CartItem, Size
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .forms import CustomLoginForm, CustomUserCreationForm
import json
from django.views.decorators.http import require_POST


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
            
            return render(request, "login.html", {"form": form})
    else:
        form = CustomLoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("index")

def cart(request):
    cart = get_cart(request)
    items = cart.items.all()
    total = cart.total_price()

    return render(request, 'cart.html', {
        "cart": cart,
        "items": items,
        "total": total,
    })

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


from django.http import JsonResponse, HttpResponseBadRequest

@require_POST
def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    variant_id = request.POST.get("variant_id")
    if not variant_id:
        return HttpResponseBadRequest("Variant must be selected.")

    variant = get_object_or_404(ProductVariant, id=variant_id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        variant=variant,
        defaults={"quantity": 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({"success": True, "quantity": cart_item.quantity})



def subtract_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    
    else:
        cart_item.delete()
    
    return redirect("cart.html")

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect("cart.html")