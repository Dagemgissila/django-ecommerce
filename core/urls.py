from django.urls import path

from . import views

app_name="core"

urlpatterns = [
    path('',views.index,name="index"),
    path('products/',views.product_list_view,name='product-list'),
    path("product/<pid>/",views.product_detail_view,name="product-detail"),
    
    # category
    path('category/',views.category_list_view,name='category-list'),
    path('category/<cid>/',views.category_product_list_view,name='category-product-list'),
    
    # vendor
    path('vendors/',views.vendor_list_view,name='vendor-list'),
    path('vendor/<vid>/',views.vendor_detail_view,name="vendor-detail")
]
