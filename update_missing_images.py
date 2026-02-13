
import os
import django
import sys
from django.core.files import File

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Handle Unicode printing
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_best_image(product_name, all_files):
    name_upper = product_name.upper().strip()
    # Synonyms and priority keywords
    synonyms = {
        'BND': 'BIND',
        'HD': 'HRD',
        'ASH': 'ASL',
        'NTR': 'NT'
    }
    
    # Remove common prefixes and split into keywords
    clean_name = name_upper.replace('DYK-', '').replace('DYN-', '').replace('PRD-', '').replace('-', ' ').replace(' -', ' ')
    keywords = [kw for kw in clean_name.split() if len(kw) > 1]
    
    # Add synonyms to keywords
    extended_keywords = list(keywords)
    for kw in keywords:
        if kw in synonyms:
            extended_keywords.append(synonyms[kw])
            
    # Try exact match first (after cleaning)
    for folder, fn in all_files:
        fn_upper = fn.upper().replace('-', '').replace(' ', '')
        if clean_name.replace(' ', '') == fn_upper or clean_name.replace(' ', '') in fn_upper:
            return os.path.join(folder, fn)
            
    # Try keyword matching (require most keywords to match, prioritize category)
    best_match = None
    max_score = 0
    
    # Define category keywords that MUST match if present
    categories = ['BIND', 'BUFFER', 'CLEAN', 'COAT', 'WET', 'SOFT', 'ZYME', 'ACID', 'ACTIV']
    target_cats = [cat for cat in categories if cat in name_upper or (cat in synonyms and synonyms[cat] in name_upper)]

    for folder, fn in all_files:
        fn_upper = fn.upper()
        
        # If product has a category, image MUST match it
        if target_cats:
            if not any(cat in fn_upper or (cat in synonyms and synonyms[cat] in fn_upper) for cat in target_cats):
                continue
        
        score = 0
        for kw in extended_keywords:
            if kw in fn_upper:
                score += 10 if kw in keywords else 5 # Higher score for original keywords
        
        if score > max_score:
            max_score = score
            best_match = os.path.join(folder, fn)
            
    if max_score > 0:
        return best_match
    return None

def update_images():
    target_names = [
        "DYK-PAD GOLD YELLOW", "BOOST OXY", "DYK -COAT KR", "DYK-ACID ANT",
        "BIOPIL AT", "DYK-ACID NTR", "BIOPIL ATM", "DYK-ACID OLL", "DYK-ACID TG",
        "DYK-ACID TPR", "DYK-ACID BF", "DYK-ACTIV CL", "DYK-ACTIV CS",
        "DYK-ACTIV PM", "DYK-ACTIV PP", "DYK-BND HD", "DYK-BND HRD",
        "DYK-BND MD", "DYK-BND MDL", "DYK-BND SFF", "DYK-BND SFT",
        "DYK-BND SRR", "DYK-BUFFER DF", "DYK-BND SRT", "DYK-BUFFER ASH",
        "DYK-BUFFER SA", "DYK-BUFFER YSS", "DYK-CARRIER ECO", "DYK-CARRIER PS",
        "DYK-BUFFER TA", "DYK-BUFFER TAK", "DYK-CLEAN 11", "DYK-CLEAN ROLL",
        "DYK-COAT EYP", "DYK-COAT EYP-B", "DYK-CLEAN OK", "DYK-CLEAN PL4",
        "DYK-COAT HD", "DYK-COAT HDD", "DYK-COAT HR", "DYK-COAT KMR",
        "DYK-COAT KMR-D", "DYK-COAT KRR", "DYK-COAT MR",
        "DYK-COAT MRD", "DYK-COAT MRD-N"
    ]

    folders = ['DYK-PAD YHG', 'DYK-WET CAN01', 'DYN-BLEACH SBX01', 'PRD-ZYME STN01']
    all_files = []
    for folder in folders:
        if os.path.exists(folder):
            for fn in os.listdir(folder):
                all_files.append((folder, fn))

    updated_count = 0
    for name in target_names:
        products = Product.objects.filter(name__iexact=name.strip())
        if not products.exists():
            # Try searching by name containing string
            products = Product.objects.filter(name__icontains=name.strip())
            
        if not products.exists():
            print(f"Product not found in DB: {name}")
            continue
            
        img_path = get_best_image(name, all_files)
        if img_path:
            for p in products:
                print(f"Updating {p.name} with {img_path}...")
                with open(img_path, 'rb') as f:
                    ext = os.path.splitext(img_path)[1]
                    p.image.save(f"{p.slug}{ext}", File(f), save=True)
                updated_count += 1
        else:
            print(f"No image found for: {name}")

    print(f"\nFinalized: Updated {updated_count} product images.")

if __name__ == "__main__":
    update_images()
