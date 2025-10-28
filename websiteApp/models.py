from django.db import models
from taggit.managers import TaggableManager
from django.utils.text import slugify

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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50, unique=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
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