from django import template

register = template.Library()


@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    keys = cart.keys()
    for key in keys:
        if int(key) == product.id:
            return cart.get(key)


@register.filter(name='price_total')
def price_total(product, cart):
    return product.price * cart_quantity(product, cart)


@register.filter(name='currency')
def currency(price):
    return "$"+str(price)


@register.filter(name='cart_total')
def cart_total(products, cart):
    sum_total = 0
    for product in products:
        sum_total += price_total(product, cart)
    return sum_total



