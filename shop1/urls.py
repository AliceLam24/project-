from django.urls import path
from . import views


app_name = 'shop1'

# urlpatterns = [
#     path('', views.product_list, name='product_list'),
#     path('Products', views.product_list, name='product_list'),
#     path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
#     path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
# ]
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:id>', views.category_list, name='category_list'),
    path('<int:id>/<int:category_id>/', views.product_detail, name='product_detail'),
    path('search/<int:id>/<int:category_id>/', views.ordering, name='ordering'),
    #path('Create_Ordering<int:id>/<int:category_id>/', views.ordering, name='ordering'),
    #path('<int:id>', views.shop1, name='shop1'),
    #path('search', views.search, name='search'),
]