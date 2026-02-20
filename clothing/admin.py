from django.contrib import admin
from .models import ClothingCategory, ClothingProduct, Size, Color

@admin.register(ClothingCategory)
class ClothingCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code')

@admin.register(ClothingProduct)
class ClothingProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'is_active')
    list_filter = ('category', 'is_available', 'is_active', 'sizes', 'colors')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'short_description')
    filter_horizontal = ('sizes', 'colors')
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug', 'image', 'hover_image', 'image_3', 'image_4', 'image_5', 'image_6', 'is_active')
        }),
        ('Product Details', {
            'fields': ('short_description', 'full_description', 'material', 'features')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'discount_price', 'is_available')
        }),
        ('Variants', {
            'fields': ('sizes', 'colors')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
    )
