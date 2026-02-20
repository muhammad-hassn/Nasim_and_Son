from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'is_active')
    list_filter = ('category', 'is_available', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'short_description')
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug', 'image', 'qr_code', 'is_active')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'discount_price', 'is_available')
        }),
        ('Content', {
            'fields': ('short_description', 'full_description', 'applications', 'benefits', 'technical_specs')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
    )
