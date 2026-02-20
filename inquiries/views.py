from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Inquiry, InquiryItem
from .cart import QuoteCart
from products.models import Product

def add_to_quote(request, product_id):
    product_type = request.POST.get('type', 'chemical')
    cart = QuoteCart(request)
    cart.add(product_id, product_type)
    messages.success(request, "Product added to quote list.")
    return redirect('inquiries:quote_list')

def update_quote(request, item_key, action):
    cart = QuoteCart(request)
    item = cart.cart.get(item_key)
    
    if item:
        current_qty = item['quantity']
        if action == 'increase':
            cart.update(item_key, current_qty + 1)
        elif action == 'decrease':
            cart.update(item_key, current_qty - 1)
            
    return redirect('inquiries:quote_list')

def remove_from_quote(request, item_key):
    cart = QuoteCart(request)
    cart.remove(item_key)
    messages.success(request, "Item removed from quote.")
    return redirect('inquiries:quote_list')

def quote_list(request):
    cart = QuoteCart(request)
    if request.method == 'POST':
        # Process Checkout
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        inquiry = Inquiry.objects.create(
            name=name, email=email, phone=phone, 
            message=message, subject="Quote Request"
        )
        
        for item in cart.get_items():
            if item['type'] == 'chemical':
                InquiryItem.objects.create(
                    inquiry=inquiry,
                    product=item['product'],
                    quantity=item['quantity']
                )
            else:
                InquiryItem.objects.create(
                    inquiry=inquiry,
                    clothing_product=item['product'],
                    quantity=item['quantity']
                )
        
        cart.clear()
        messages.success(request, "Your quote request has been sent!")
        return redirect('core:home')
        
    from blog.models import BlogPost
    latest_posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:3]
    return render(request, 'inquiries/quote_list.html', {
        'cart_items': cart.get_items(),
        'latest_posts': latest_posts
    })
