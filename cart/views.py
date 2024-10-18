from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    shop_id = product.shop_id
    print('Product Shop ID :', shop_id)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data

        # product_desc = request.POST.get('product_desc')  # Retrieve product_desc from POST data
        print('product_id: ' + str(product_id))
        print('quantity: ' + str(cd['quantity']))
        
        if shop_id == 1 :
            cart.add(product=product,
                 quantity=cd['quantity'],
                 product_desc= "product_desc_desc",   # add product description or other field
                 override_quantity=cd['override']                 
                 )
            print('cart shop 1 transaction added :' )

        if shop_id == 2 :
            cart.add(product=product,
                 quantity=cd['quantity'],
                 product_desc= cd['product_desc'],   # add product description or other field
                 override_quantity=cd['override']                 
                 )
            print('cart shop 2 transaction added : ', cd['product_desc'] )

        if shop_id == 3 :

            date=request.POST.get('date')
            guests = request.POST.get('guests')
            time_slot = request.POST.get('time_slot')
            studio_name = request.POST.get('studio_name')
            studio_address = request.POST.get('studio_address')
            studio_district = request.POST.get('studio_district')

            guest_wording = f"{guests}"

            format_product_desc = (
                f"DIY baking package\n"
                f"-------------------------\n"
                f"Studio: {studio_name}\n"
                f"[{studio_address}, {studio_district}]\n"
                f"-------------------------\n"
                f"Date: {date}\n"
                f"Time Slot: {time_slot}\n"
                f"Guest(s): {guest_wording}\n"
                ) 
            
            cart.add(product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override'],            
                product_desc = format_product_desc,
                date=date,
                guests=guests,
                time_slot=time_slot,
                studio_name=studio_name,
                studio_address=studio_address,
                studio_district=studio_district
                )
            
            print('shop 3 Cart transaction added :' , format_product_desc )

        if shop_id == 4 :
            cart.add(product=product,
                 quantity=cd['quantity'],
                 product_desc= product.name,   # add product description or other field
                 override_quantity=cd['override']                 
                 )
            print('cart shop 4 transaction added :' , product.name)
        
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
       item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'product_desc': item['product_desc'],
                                                                   'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})
