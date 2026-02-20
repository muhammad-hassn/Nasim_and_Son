from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from products.models import SEOModel

class ClothingCategory(SEOModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='clothing/categories/', blank=True, null=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Clothing Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('clothing:category_detail', args=[self.slug])

class Size(models.Model):
    name = models.CharField(max_length=50) # e.g. S, M, L, XL, 32, 34
    
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7, blank=True, help_text="e.g. #FFFFFF")
    
    def __str__(self):
        return self.name

class ClothingProduct(SEOModel):
    category = models.ForeignKey(ClothingCategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='clothing/products/', help_text="Main Image")
    hover_image = models.ImageField(upload_to='clothing/products/', blank=True, null=True, help_text="Hover Image / 2nd View")
    image_3 = models.ImageField(upload_to='clothing/products/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='clothing/products/', blank=True, null=True)
    image_5 = models.ImageField(upload_to='clothing/products/', blank=True, null=True)
    image_6 = models.ImageField(upload_to='clothing/products/', blank=True, null=True)
    
    short_description = models.TextField(help_text="Shown in listing")
    full_description = models.TextField()
    material = models.CharField(max_length=255, blank=True)
    features = models.TextField(blank=True, help_text="Bullet points")
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    sizes = models.ManyToManyField(Size, blank=True)
    colors = models.ManyToManyField(Color, blank=True)
    
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('clothing:product_detail', args=[self.slug])
