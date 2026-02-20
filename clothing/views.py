from django.shortcuts import render, get_object_or_404
from .models import ClothingCategory, ClothingProduct

def clothing_list(request, category_slug=None):
    category = None
    categories = ClothingCategory.objects.all()
    products = ClothingProduct.objects.filter(is_active=True)
    
    if category_slug:
        category = get_object_or_404(ClothingCategory, slug=category_slug)
        products = products.filter(category=category)
    
    # Simple filtering Example
    size = request.GET.get('size')
    color = request.GET.get('color')
    if size:
        products = products.filter(sizes__name=size)
    if color:
        products = products.filter(colors__name=color)

    return render(request, 'clothing/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })

def clothing_detail(request, slug):
    product = get_object_or_404(ClothingProduct, slug=slug, is_active=True)
    related_products = ClothingProduct.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'clothing/detail.html', {
        'product': product,
        'related_products': related_products
    })
