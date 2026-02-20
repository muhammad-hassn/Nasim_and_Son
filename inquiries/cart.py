from products.models import Product
from clothing.models import ClothingProduct

class QuoteCart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('quote_cart')
        if not cart:
            cart = self.session['quote_cart'] = {}
        self.cart = cart

    def add(self, product_id, product_type='chemical'):
        item_key = f"{product_type}_{product_id}"
        if item_key not in self.cart:
            self.cart[item_key] = {
                'id': product_id,
                'type': product_type,
                'quantity': 1
            }
        else:
            self.cart[item_key]['quantity'] += 1
        self.save()

    def update(self, item_key, quantity):
        if item_key in self.cart:
            if quantity > 0:
                self.cart[item_key]['quantity'] = int(quantity)
            else:
                self.remove(item_key)
            self.save()

    def remove(self, item_key):
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def save(self):
        self.session.modified = True

    def get_items(self):
        items = []
        for key, value in self.cart.items():
            if value['type'] == 'chemical':
                product = Product.objects.filter(id=value['id']).first()
                if product:
                    items.append({
                        'key': key,
                        'product': product,
                        'type': 'chemical',
                        'quantity': value['quantity']
                    })
            elif value['type'] == 'clothing':
                product = ClothingProduct.objects.filter(id=value['id']).first()
                if product:
                    items.append({
                        'key': key,
                        'product': product,
                        'type': 'clothing',
                        'quantity': value['quantity']
                    })
        return items
    
    def clear(self):
        self.session['quote_cart'] = {}
        self.save()
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
