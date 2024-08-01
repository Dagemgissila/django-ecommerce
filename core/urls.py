from django.urls import path

from . import views

app_name="core"

urlpatterns = [
    path('',views.index,name="index"),
    path('products/',views.product_list_view,name='product-list'),
    path("product/<pid>/",views.product_detail_view,name="product-detail"),
    path("products/tag/<slug:tag_slug>/", views.tag_list, name="tags"),
    path('filter-product/',views.filter_products, name='filter-product'),
    path("add-to-cart", views.add_to_cart, name="add-to-cart"),
    
    
    # category
    path('category/',views.category_list_view,name='category-list'),
    path('category/<cid>/',views.category_product_list_view,name='category-product-list'),
    
    # vendor
    path('vendors/',views.vendor_list_view,name='vendor-list'),
    path('vendor/<vid>/',views.vendor_detail_view,name="vendor-detail"),
    
    path("ajax-add-review/<str:pid>/",views.ajax_add_review,name="ajax-add-review"),
    path("search/",views.search_view,name="search")
    
]
