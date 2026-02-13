
import os
import django
import pandas as pd
from django.utils.text import slugify
from django.core.files import File
import shutil
import sys

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Handle Unicode printing
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from products.models import Product, Category

def get_or_create_category(name):
    if not name or pd.isna(name):
        name = "Uncategorized"
    slug = slugify(name)[:50]
    cat, created = Category.objects.get_or_create(name=name, defaults={'slug': slug})
    return cat

def find_product_image(product_name):
    folders = ['DYK-PAD YHG', 'DYK-WET CAN01', 'DYN-BLEACH SBX01', 'PRD-ZYME STN01']
    # Try exact match or partial match
    search_name = product_name.strip().upper()
    for folder in folders:
        if not os.path.exists(folder):
            continue
        for filename in os.listdir(folder):
            fname_upper = filename.upper()
            if search_name in fname_upper or fname_upper.startswith(search_name):
                return os.path.join(folder, filename)
    return None

def import_data():
    # Cleanup existing products for a clean import
    print("Cleaning up existing products...")
    Product.objects.all().delete()
    
    excel_path = 'Updated FILE WITH QR CODE NUMBER.xlsx'
    if not os.path.exists(excel_path):
        print(f"Excel file not found: {excel_path}")
        return

    df = pd.read_excel(excel_path)
    print(f"Found {len(df)} products in Excel.")

    qr_folder = "QRCode_49D7D0D19AA8CE78E0630100007F4489_02-02-2026 12_53_55"
    
    count = 0
    for index, row in df.iterrows():
        p_name = str(row['Product Name']).strip()
        zdhc_pid = str(row['ZDHC PID']).strip()
        cat_name = str(row['Category']).strip()
        p_type = str(row['Type']).strip()
        
        cat = get_or_create_category(cat_name)
        
        # Create a unique slug
        base_slug = slugify(p_name)
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        print(f"Importing {p_name} ({zdhc_pid})...")
        
        product = Product.objects.create(
            name=p_name,
            slug=slug,
            category=cat,
            short_description=f"{p_name} is a high-performance chemical solution specifically formulated for {p_type}.",
            full_description=f"{p_name} is an advanced industrial formulation designed for optimized results in {cat_name} processes. This ZDHC-certified product ensures high purity and consistent performance in demanding manufacturing environments.",
            applications=f"- Primary use in {p_type}\n- Recommended for industrial-scale {cat_name}",
            benefits=f"- ZDHC Certified\n- High Purity Level\n- Consistent Quality",
            technical_specs=f"ZDHC PID: {zdhc_pid}\nCategory: {cat_name}\nType: {p_type}",
            is_active=True
        )
        
        # QR Code
        qr_filename = f"QRCode_{zdhc_pid}_02-02-2026.png"
        qr_path = os.path.join(qr_folder, qr_filename)
        if os.path.exists(qr_path):
            with open(qr_path, 'rb') as f:
                product.qr_code.save(qr_filename, File(f), save=False)
        
        # Main Product Image (from root folders)
        img_path = find_product_image(p_name)
        if img_path:
            with open(img_path, 'rb') as f:
                ext = os.path.splitext(img_path)[1]
                product.image.save(f"{slug}{ext}", File(f), save=False)
        else:
            # Try searching with just the part after 'DYK-' if applicable
            if p_name.startswith('DYK-'):
                img_path = find_product_image(p_name.replace('DYK-', ''))
                if img_path:
                    with open(img_path, 'rb') as f:
                        ext = os.path.splitext(img_path)[1]
                        product.image.save(f"{slug}{ext}", File(f), save=False)

        product.save()
        count += 1
        if count % 50 == 0:
            print(f"Processed {count} products...")

    print(f"Successfully imported {count} products.")

if __name__ == "__main__":
    import_data()
