from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, ProductSitemap, CategorySitemap, BlogSitemap

# Admin Site Customization
admin.site.site_header = "Nasim and Son Administrator"
admin.site.site_title = "Nasim and Son Admin Portal"
admin.site.index_title = "Welcome to Nasim and Son Management"

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('product/', include('products.urls')),
    path('clothing/', include('clothing.urls')),
    path('blog/', include('blog.urls')),
    path('inquiry/', include('inquiries.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
