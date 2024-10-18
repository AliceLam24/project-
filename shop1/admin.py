from django.contrib import admin

# Register your models here.
from .models import Cakes, ProductDetail, Ordering

class CakesAdmin(admin.ModelAdmin):
    list_display = ('id', 'Cake_Sizes', 'Cake_Weight', 'Cake_Desc')
    list_display_links = ('id', 'Cake_Desc')
    search_fields = ('id',)
    list_per_page = 10
admin.site.register(Cakes, CakesAdmin)

class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'allergen', 'First_size', 'First_weight', 'First_desc', 'First_price', 'Second_size', 'Second_weight', 'Second_desc', 'Second_price', 'Third_size', 'Third_weight', 'Third_desc', 'Third_price', 'Fourth_size', 'Fourth_weight', 'Fourth_desc', 'Fourth_price', 'product_id')
    list_display_links = ('id', 'product_id')
    search_fields = ('id',)
    list_per_page = 10
admin.site.register(ProductDetail, ProductDetailAdmin)

class OrderingAdmin(admin.ModelAdmin):
    list_display = ('id', 'OrderingDT', 'OrderingConfirm')
    list_display_links = ('id','OrderingDT')
    list_per_page = 10
admin.site.register(Ordering, OrderingAdmin)
