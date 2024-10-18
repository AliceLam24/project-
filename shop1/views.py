import calendar
from django.shortcuts import render, get_object_or_404, redirect
from cart.forms import CartAddProductForm
from shop.models import Category, Product
from shop1.models import ProductDetail, Ordering
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from datetime import datetime, timedelta
from .forms import Create_Ordering
from django.utils import timezone
from cart.cart import Cart
from cart.forms import CartAddProductForm
from decimal import Decimal
from django.conf import settings
from django.contrib.sessions.models import Session
import json
from decimal import Decimal
import uuid

def generate_uuid_key():
    return str(uuid.uuid4())

#<Hard Code Table> from listings.choices import price_choices, bedroom_choices, district_choices


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.filter(shop_id=1).order_by('id')
        
    #! Display all available products
    #listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    #products = Product.objects.filter(available=True)[:Number of records display]
    products = Product.objects.filter(available=True, shop_id=1).order_by('name')
    
    print("[product_list] No. of categories:" , len(categories))
    print("[product_list] No. of products:" , len(products))
    
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    # @ pass database records into listings context
 
    context = {
                'category': category,
                'products': products,
                'categories': categories,
    }
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop1/product/list.html',
                  context)
                  

def category_list(request, id, category_slug=None):
    category = None
    #! Display all categories
    categories = Category.objects.filter(shop_id=1)
    CategoryName = Category.objects.get(id=id)
    
    print("[category_detail] Categories Name:" , CategoryName)

    #! Display all available products
    #listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    #products = Product.objects.filter(available=True)[:Number of records display]
    products = Product.objects.filter(available=True, category_id=id)
    
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    # @ pass database records into listings context
    #context = {'products': paged_products}
    
    print("[category_detail] Categories Name:" , CategoryName)
    
    context = {
                'category': category,
                'products': products,
                'category_name': CategoryName
    }
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop1/product/category.html',
                   context)


def product_detail(request, id, category_id):
    
    product = get_object_or_404(Product,
                                id=id)
    
    CategoryName = Category.objects.get(id=category_id)
    

    ProductDetail = ProductDetail.objects.filter(product_id_id=id)

    ProductDetail_Item = product.name

    if ProductDetail:
        print("ProductDetail_Item:" , ProductDetail_Item)
        print("Categories Name:" , CategoryName)
    
    cart_product_form = CartAddProductForm()
   
    dDeliveryDateList = {}
    x = range(2, 14)
    for n in x:
        pday01 = datetime.now()
        pdayN = pday01 + timedelta(n)
        dDeliveryDateList[n] = pdayN.strftime('%Y-%m-%d') + " , " + pdayN.strftime('%A')
        
        print("Day", n, pdayN.strftime('%Y-%m-%d'))
        print("Day", pdayN.strftime('%A'))   

    present_day = datetime.now()
    Earliest_date = present_day + timedelta(2)
    print("present_day", present_day.strftime ('%Y-%m-%d'))    
    print("DeliveryDate.items", dDeliveryDateList)

    return render(request,
                  'shop1/product/detail.html',
                  {'product': product,
                   'category': CategoryName,
                   'cart_product_form': cart_product_form,
                   'ProductDetail_Item': ProductDetail_Item,
                   'present_day': present_day,
                   'fastest': Earliest_date,
                   'DeliveryDate': dDeliveryDateList})
    

def ordering(request, id, category_id):
    print("ordering: [request.POST]" , request.POST) 
    

    if request.method == 'POST':
        form = Ordering(request.POST)
        
        ContactPerson = request.POST.get('ContactPerson').strip()
        ContactNumber = request.POST.get('ContactNumber').strip()
        ContactEmail = request.POST.get('ContactEmail').strip()
        Qty = int(request.POST.get('Qty'))

        if 'CakeSizeWeightPrice' in request.POST:
            input_string = request.POST.get('CakeSizeWeightPrice')
            parts = input_string.split("/")
            CakeSize = parts[0]
            CakeSize = CakeSize.strip()
            CakeWeight = parts[1]
            CakeWeight = CakeWeight.strip()
            CakeDesc = parts[2]
            CakeDesc = CakeDesc.strip()
            CakePrice = int(parts[3])

        if 'PickupDelivery' in request.POST:
            input_string = request.POST.get('PickupDelivery')
            parts = input_string.split("/")
            PickupDelivery = parts[0]
            PickupDelivery = PickupDelivery.strip()
            DeliveryCharges = int(parts[1])

        if 'PickupDeliveryDate' in request.POST:
            dDeliveryDateList = {}
            PickupDeliveryDate = request.POST.get('PickupDeliveryDate')
            print("request.POST.get('PickupDeliveryDate')", request.POST.get('PickupDeliveryDate'))

            x = range(2, 14)
            for n in x:
                pday01 = datetime.now()
                pdayN = pday01 + timedelta(n)
                dDeliveryDateList[n] = pdayN.strftime('%Y-%m-%d')
                print(n , dDeliveryDateList[n])
                print("dDeliveryDateList[PickupDeliveryDate]", n, pdayN.strftime('%Y-%m-%d'))  

            PickupDeliveryDate = dDeliveryDateList[int(request.POST.get('PickupDeliveryDate'))]
            print("dDeliveryDateList[PickupDeliveryDate]", dDeliveryDateList[int(request.POST.get('PickupDeliveryDate'))])
            present_day = datetime.now()
            fastest = present_day + timedelta(2)
            
            print("present_day", present_day)  
            print("DeliveryDate.items", dDeliveryDateList)

        
        PickupDeliveryTime = request.POST.get('PickupDeliveryTime').strip()
        DeliveryAddr = request.POST.get('DeliveryAddress').strip()  
        Amount = (int(Qty) * int(CakePrice)) + int(DeliveryCharges)   
        Product_id = int(id)
        Category_id = int(category_id)

        OrderingDT = datetime.now()


        # for generation of key linking the product detail
        uuid_key = generate_uuid_key()
        print(uuid_key)        

        
        context = {
            'OrderingDT': OrderingDT,
            'OrderingConfirm': False,
            'ContactPerson': ContactPerson,
            'ContactNumber': ContactNumber,
            'ContactEmail': ContactEmail,
            'Qty': Qty,
            'CakeSize': CakeSize,
            'CakeWeight': CakeWeight,
            'CakeDesc': CakeDesc,
            'CakePrice': CakePrice,
            'PickupDelivery': PickupDelivery,
            'PickupDeliveryTime': PickupDeliveryTime,
            'PickupDeliveryDate': PickupDeliveryDate,
            'DeliveryAddr': DeliveryAddr,
            'DeliveryCharges': DeliveryCharges,
            'OrderAmount': Amount,
            'Product_id': Product_id,
            'Category_id': Category_id
            }

        # to to confirmation page


        print(" ---context---:", context)
        print("form.is_valid()", form.is_valid())
    if form.is_valid():
        
        #---------------- Tbl: Ordering ---------------- 
        print("//form.is_valid //" ,context) 
        #form.save()  # Save the form data to the database 
        
        new_order = Ordering.objects.create(
                    ContactPerson = ContactPerson,
                    ContactNumber = ContactNumber,
                    ContactEmail = ContactEmail,
                    Qty = Qty,
                    CakeSize = CakeSize,
                    CakeWeight = CakeWeight,
                    CakeDesc = CakeDesc,
                    CakePrice = CakePrice,
                    PickupDelivery = PickupDelivery,
                    PickupDeliveryTime = PickupDeliveryTime,
                    PickupDeliveryDate = PickupDeliveryDate,
                    DeliveryAddr = DeliveryAddr,
                    DeliveryCharges = DeliveryCharges,
                    OrderAmount = Amount,
                    Product_id = Product_id,
                    Category_id = Category_id,
                    Session_Key = request.session.session_key)
        new_order_id = new_order.id  # Get the ID of the newly created record
            
        print("---New Ordering ID--- ",new_order_id)
        print("session_id:", request.session.session_key)
            
        Msg = "Add to the cart!"
        
        print("----Cart----", new_order)
        
        #return redirect('success')  # Redirect after saving
        
        cart = []
        session_key = []
        
        if 'Msg' in locals():
            # Loading Cart
            print("'Msg' in locals()", 'Msg' in locals())
            if Msg is not None:
                queryset_list = Ordering.objects.order_by('-OrderingDT')
                
                sessions = Session.objects.all()

                for session in sessions:
                    # Now you can access the raw session data as a dictionary
                    print(f"Session Key: {session.session_key}")
                    session_key = {session.session_key}
                    if session.session_key == request.session.session_key:
                        print(f"Session Data: {session.get_decoded()}")
                        cart = session.get_decoded()
                        print(f"Expire Date: {session.expire_date}")
                        print("****************************************************************************")

                print("request.session.session_key)", request.session.session_key)
             
            
            CategoryName = Category.objects.get(id=category_id)
            Orderings_queryset_list = queryset_list.filter(
                Session_Key__iexact=request.session.session_key)
            
            print("id:" , id)
            print("Product_id:" , Product_id)
            Products = Product.objects.filter(id=Product_id).values()
            #if Products.objects.filter(id=Product_id).exists():
            #    print("[product_detail] ProductDetail_Item:" , Products)
            
            
                    
            return render(request,
                    'shop1/product/ordering.html',{
                    'Products': get_object_or_404(Product, id=Product_id),
                    'Categories': get_object_or_404(Category, id=Category_id),
                    'Orderings': Orderings_queryset_list,
                    'ContactPerson': ContactPerson,
                    'ContactNumber': ContactNumber,
                    'ContactEmail': ContactEmail,
                    'Qty': Qty,
                    'CakeSize': CakeSize,
                    'CakeWeight': CakeWeight,
                    'CakeDesc': CakeDesc,
                    'CakePrice': CakePrice,
                    'PickupDelivery': PickupDelivery,
                    'PickupDeliveryTime': PickupDeliveryTime,
                    'PickupDeliveryDate': PickupDeliveryDate,
                    'DeliveryAddr': DeliveryAddr,
                    'DeliveryCharges': DeliveryCharges,
                    'OrderAmount': Amount,
                    'Product_id': Product_id,
                    'Category_id': Category_id,
                    'Session_Key': request.session.session_key,
                    'new_order_id': new_order.id,
                    'Msg': Msg,
                    'Orderings': queryset_list,
                    'total' : len(queryset_list),
                    'cart': cart,
                    'session_key' : session_key})
    else:
        print("Form errors:", form.errors)  # This will show you the validation errors
        form = Ordering()
    

    # Here to next page

    return render(request, 'shop1/product/ordering.html', {'form': form})