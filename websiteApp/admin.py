from django.contrib import admin
from .models import Category, Product, ProductImage, Size, Color, ProductVariant

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'IsInStock')
    list_filter = ('category', 'IsInStock', 'fit_type')
    search_fields = ('title', 'description', 'sku')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline, ProductVariantInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'stock')

