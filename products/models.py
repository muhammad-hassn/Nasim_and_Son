from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class SEOModel(models.Model):
    meta_title = models.CharField(max_length=255, blank=True, help_text="SEO Title")
    meta_description = models.TextField(blank=True, help_text="SEO Description")
    
    class Meta:
        abstract = True

class Category(SEOModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category_products', args=[self.slug])

class Product(SEOModel):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='products/')
    short_description = models.TextField(help_text="Shown in list view")
    full_description = models.TextField(help_text="Start with what the product is")
    applications = models.TextField(blank=True, help_text="Bullet points or text")
    benefits = models.TextField(blank=True)
    technical_specs = models.TextField(blank=True, help_text="Table or list of specs")
    
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
        return reverse('products:product_detail', args=[self.slug])
