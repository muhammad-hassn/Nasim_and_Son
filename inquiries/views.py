from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Inquiry, InquiryItem
from .cart import QuoteCart
from products.models import Product

def add_to_quote(request, product_id):
    cart = QuoteCart(request)
    cart.add(product_id)
    messages.success(request, "Product added to quote list.")
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
            InquiryItem.objects.create(
                inquiry=inquiry,
                product=item['product'],
                quantity=item['quantity']
            )
        
        cart.clear()
        messages.success(request, "Your quote request has been sent!")
        return redirect('core:home')
        
    return render(request, 'inquiries/quote_list.html', {'cart_items': cart.get_items()})
