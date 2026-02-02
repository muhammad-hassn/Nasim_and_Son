from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from products.models import Product, Category
from blog.models import BlogPost

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['core:home', 'core:company', 'core:contact', 'products:landing', 'blog:list']

    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    
    def items(self):
        return Category.objects.all()

class BlogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    
    def items(self):
        return BlogPost.objects.filter(is_published=True)
    
    def lastmod(self, obj):
        return obj.created_at
