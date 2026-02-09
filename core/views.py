from django.shortcuts import render, redirect
from django.contrib import messages
from inquiries.models import Inquiry
from products.models import Category, Product
from blog.models import BlogPost

def home(request):
    categories = Category.objects.all()[:6]
    featured_products = Product.objects.filter(is_active=True)[:4]
    latest_posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:3]
    return render(request, 'core/home.html', {
        'categories': categories,
        'featured_products': featured_products,
        'latest_posts': latest_posts
    })

def company(request):
    return render(request, 'core/company.html')

from .models import Certificate

def certificates(request):
    latest_cert = Certificate.objects.all().first()
    if latest_cert and latest_cert.pdf_file:
        return redirect(latest_cert.pdf_file.url)
    return render(request, 'core/certificates.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        Inquiry.objects.create(
            name=name, email=email, phone=phone,
            subject=subject, message=message
        )
        messages.success(request, "Thank you! Your message has been sent.")
        return redirect('core:contact')
        
    return render(request, 'core/contact.html')
