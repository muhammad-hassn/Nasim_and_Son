from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'blog/list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related_posts = BlogPost.objects.filter(category=post.category).exclude(id=post.id)[:3]
    return render(request, 'blog/detail.html', {'post': post, 'related_posts': related_posts})
