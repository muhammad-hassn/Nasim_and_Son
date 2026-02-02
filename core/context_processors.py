from inquiries.cart import QuoteCart

def nasim_global_context(request):
    cart = QuoteCart(request)
    return {
        'cart_count': len(cart),
        'company_name': 'Nasim and Sons',
        'meta_site_domain': 'nasimandsons.com'
    }
