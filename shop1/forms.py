from django import forms
from .models import Ordering

class Create_Ordering(forms.ModelForm):
    class Meta:
        model = Ordering
        #fields = ['id', 'OrderingDT', 'OrderingConfirm', 'ContactPerson', 'ContactNumber', 'Qty', 'CakeSize', 'CakeWeight', 'CakeDesc', 'PickupDelivery', 'PickupDeliveryTime', 'DeliveryAddr', 'DeliveryCharges', 'product_id', 'ContactEmail', 'category_id', 'CakePrice', 'OrderAmount']
        
        # 'id', 'OrderingConfirm', 'OrderingDT' is omitted
        #fields = ['ContactPerson', 'ContactNumber', 'Qty', 'CakeSize', 'CakeWeight', 'CakeDesc', 'PickupDelivery', 'PickupDeliveryTime', 'DeliveryAddr', 'DeliveryCharges', 'product_id', 'ContactEmail', 'category_id', 'CakePrice', 'OrderAmount']
        
        fields = [
                    'ContactPerson',
                    'ContactNumber',
                    'ContactEmail',
                    'Qty',
                    'CakeSize',
                    'CakeWeight',
                    'CakeDesc',
                    'CakePrice',
                    'PickupDelivery',
                    'PickupDeliveryTime',
                    'PickupDeliveryDate',
                    'DeliveryAddr',
                    'DeliveryCharges',
                    'OrderAmount',
                    'Category_id',
                    'Product_id',
                    'Session_Key'
        ]