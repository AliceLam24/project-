from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def is_new_order_item(self, current_item, new_item):
        """
        Check if the new item should be considered as a new order item.
        """
        if current_item.get('studio_name') != new_item.get('studio_name'):
            return True
        if current_item.get('date') != new_item.get('date'):
            return True
        if current_item.get('time_slot') != new_item.get('time_slot'):
            return True
        if current_item.get('guests') != new_item.get('guests'):
            return True
        return False

    def add(self, product, product_desc, studio_name=None, studio_district=None, studio_address=None, date=None, time_slot=None, guests=None, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        new_item = {
            'product': product.id,
            'quantity': 0,
            'product_desc': product_desc,
            'price': str(product.price),
            'studio_name': studio_name,
            'studio_address': studio_address,
            'studio_district': studio_district,
            'date': date,
            'time_slot': time_slot,
            'guests': guests
        }

        # Check if the item already exists in the cart
        for key, current_item in list(self.cart.items()):
            if current_item['product'] == new_item['product']:
                if self.is_new_order_item(current_item, new_item):
                    # Overwrite the old item if it is considered a new order item
                    self.cart[key] = new_item
                    self.cart[key]['quantity'] = quantity
                    self.save()
                    return
                else:
                    # Update the quantity of the existing item
                    if override_quantity:
                        current_item['quantity'] = quantity
                    else:
                        current_item['quantity'] += quantity
                    self.save()
                    return

        # Add the new item to the cart
        self.cart[product_id] = new_item
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())