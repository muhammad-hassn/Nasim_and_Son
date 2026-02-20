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

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
import io
from PIL import Image

class ClothingProduct(SEOModel):
    category = models.ForeignKey(ClothingCategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='clothing/products/', help_text="Main Image (Recommended: 3:4 ratio, e.g., 800x1066px)")
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

    def clean(self):
        super().clean()
        image_fields = [self.image, self.hover_image, self.image_3, self.image_4, self.image_5, self.image_6]
        for field in image_fields:
            if field:
                try:
                    img = Image.open(field)
                    w, h = img.size
                    
                    # 1. Minimum dimensions check
                    if w < 300 or h < 300:
                        raise ValidationError(f"Image '{field.name}' is too small. Minimum 300x300px required.")
                    
                    # 2. Aspect ratio check (Target: 0.75 +/- 0.1 tolerance)
                    # We'll allow some flexibility but reject extreme landscape/square
                    ratio = w / h
                    if ratio > 0.9: # Closer to square or landscape
                        raise ValidationError(f"Image '{field.name}' must be in portrait orientation (Recommended ratio 3:4).")
                except Exception as e:
                    if isinstance(e, ValidationError): raise e
                    pass

    def process_image(self, image_field):
        """Helper to resize and optimize images to 800x1066 (3:4)"""
        if not image_field: return
        
        img = Image.open(image_field)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Target size
        target_w = 800
        target_h = int(target_w / (3/4)) # 1066px
        
        # Resize using thumbnail to maintain ratio, then crop
        img.thumbnail((target_w, 2000), Image.Resampling.LANCZOS)
        
        # Center crop to 3:4 if needed
        w, h = img.size
        left = 0
        top = (h - target_h) / 2
        right = w
        bottom = top + target_h
        
        if h > target_h:
            img = img.crop((left, top, right, bottom))
        
        # Save to buffer
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=85, optimize=True)
        filename = image_field.name.split('/')[-1]
        if not filename.endswith('.jpg'):
            filename = filename.rsplit('.', 1)[0] + '.jpg'
            
        return ContentFile(buffer.getvalue(), name=filename)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            
        # Process and optimize all images before saving
        image_fields = ['image', 'hover_image', 'image_3', 'image_4', 'image_5', 'image_6']
        for field_name in image_fields:
            field = getattr(self, field_name)
            
            # Check if this is a new file being uploaded
            if field and hasattr(field, 'file') and not isinstance(field.file, (io.BytesIO, bytes)):
                try:
                    processed_image = self.process_image(field)
                    if processed_image:
                        setattr(self, field_name, processed_image)
                except Exception as e:
                    print(f"Error processing {field_name}: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('clothing:product_detail', args=[self.slug])
