from django.db import models
from taggit.managers import TaggableManager
from django.utils.text import slugify
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    #generate slug if there isnt one
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, related_name='products'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50, unique=True)
    stock = models.PositiveIntegerField(default=0)
    IsInStock = models.BooleanField(default=True)
    fit_type = models.CharField(
        max_length=50,
        choices=[
            ('regular', 'Regular Fit'),
            ('slim', 'Slim Fit'),
            ('baggy', 'Baggy Fit'),
            ('oversized', 'Oversized Fit'),
        ],
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    @property
    def image0(self):
        """ returns the first image associated with the product, or none """
        first_image = self.images.first()
        return first_image.image if first_image else None
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        self.IsInStock = self.stock > 0
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="product_images/")
    order = models.PositiveIntegerField(default=0, help_text="Set the display order. 0 will be the primary image.")

    def __str__(self):
        return f"Image For {self.product.title}"
    
    class Meta:
        """Defines the default ordering for image queries."""
        ordering = ['order']
    

class Size(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name
    
class Color(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

    

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)

class Sale(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (Active: {self.is_active})"
    @property
    def is_currently_active(self):
        """return true if sale is active based on real time"""
        current_time = now()
        if not self.is_active:
            return False
        if self.start_date and current_time < self.start_date:
            return False
        if self.end_date and current_time > self.end_date:
            return False
        return True
    

class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    session_key = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart {self.pk} for {self.user}"
        return f"Cart {self.pk} for session {self.session_key}"

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "variant")

    def subtotal(self):
        if self.variant:
            return self.variant.product.price * self.quantity
        else:
            return self.product.price * self.quantity


    def __str__(self):
        return f"{self.quantity} x {self.product.title} in Cart {self.cart.pk}"


    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """create and return regular user with email and password"""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No username, just email + password

    objects = CustomUserManager()

    def __str__(self):
        return self.email

