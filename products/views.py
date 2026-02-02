from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Category, Product

def product_landing(request):
    categories = Category.objects.all()
    return render(request, 'products/landing.html', {'categories': categories})

def product_resolver(request, slug):
    # Try to find a category first
    try:
        category = Category.objects.get(slug=slug)
        # It's a category
        products = category.products.filter(is_active=True)
        return render(request, 'products/category_detail.html', {
            'category': category,
            'products': products
        })
    except Category.DoesNotExist:
        # Try to find a product
        product = get_object_or_404(Product, slug=slug, is_active=True)
        # It's a product
        related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
        return render(request, 'products/product_detail.html', {
            'product': product,
            'related_products': related_products
        })
