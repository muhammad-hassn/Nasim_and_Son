from products.models import Product

class QuoteCart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('quote_cart')
        if not cart:
            cart = self.session['quote_cart'] = {}
        self.cart = cart

    def add(self, product_id):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1}
        else:
            self.cart[product_id]['quantity'] += 1
        self.save()

    def update(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            if quantity > 0:
                self.cart[product_id]['quantity'] = int(quantity)
            else:
                self.remove(product_id)
            self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def get_items(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        items = []
        for product in products:
            items.append({
                'product': product,
                'quantity': self.cart[str(product.id)]['quantity']
            })
        return items
    
    def clear(self):
        del self.session['quote_cart']
        self.save()
    
    def __len__(self):
        return len(self.cart)
