from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]

PERSON_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 5)]

class CartAddProductForm(forms.Form):
    
    product_desc = forms.CharField(
        required=False,
        label="",  # Set the label
        widget=forms.Textarea(attrs={
            'readonly': 'readonly',
            'style': 'border: none; background: none; width: auto;',
            'maxlength': '80',  # This will limit the total number of characters
            'rows': '4',  # This will define the number of visible rows
            'wrap': 'soft'
        })
    )
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
    
    #  For shop 3
    
    
    
    # for shop 1
    

