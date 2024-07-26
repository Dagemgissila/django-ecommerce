from django.shortcuts import render
from core.models import CartOrderItems, Product, Category, Vendor, CartOrder, ProductImages, ProductReview, wishlist_model, Address
# Create your views here.

def index(request):
    products=Product.objects.all().order_by("-id")
    context={
        'products':products
    }
    return render(request,"core/index.html",context)

