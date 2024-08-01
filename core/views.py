from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from core.models import CartOrderItems, Product, Category, Vendor, CartOrder, ProductImages, ProductReview, wishlist_model, Address
from django.db.models import Count,Avg
from taggit.models import Tag
from core.forms import ProductReviewForm
from django.db.models import Q
from django.template.loader import render_to_string

# Create your views here.


def index(request):
    products=Product.objects.filter(product_status="published",featured=True).order_by("-id")
    context={
        'products':products
    }
    return render(request,"core/index.html",context)

def product_list_view(request):
    products=Product.objects.filter(product_status="published").order_by("-id")
    context={
        'products':products
    }
    return render(request,"core/product-list.html",context)   

def category_list_view(request):
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    return render(request,'core/category-list.html',context)

    

def category_product_list_view(request,cid):
    category=Category.objects.get(cid=cid)
    products=Product.objects.filter(product_status="published",category=category)
    
    context={
        'category':category,
        "products":products
    }
    return render(request,'core/category-product-list.html',context)


def vendor_list_view(request):
    vendors=Vendor.objects.all()
    context={
        "vendors":vendors
    }
    
    return render(request,'core/vendor-list.html',context)

def vendor_detail_view(request,vid):
    vendor=Vendor.objects.get(vid=vid)
    products=Product.objects.filter(vendor=vendor,product_status="published")
    categories=Category.objects.all()
    context={
        "vendor":vendor,
        "products":products,
        "categories":categories
    }
    
    return render(request,'core/vendor-detail.html',context)


def product_detail_view(request,pid):
    product=Product.objects.get(pid=pid)
    products=Product.objects.filter(category=product.category).exclude(pid=pid)
    reviews=ProductReview.objects.filter(product=product).order_by("-date")
    average_rating=ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
    review_form=ProductReviewForm()
    make_review=True
    if request.user.is_authenticated:
        user_review_count=ProductReview.objects.filter(user=request.user,product=product).count()
        
        if user_review_count > 0:
            make_review=False
        
    p_image=product.p_images.all()
    
    context={
        "p":product,
        'p_image':p_image,
        'make_review':make_review,
        "products":products,
        "reviews":reviews,
        "average_rating":average_rating,
        "review_form":review_form
    }
    
    return render(request,"core/product-detail.html",context)

def tag_list(request, tag_slug=None):

    products = Product.objects.filter(product_status="published").order_by("-id")

    tag = None 
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products": products,
        "tag": tag
    }

    return render(request, "core/tag.html", context)


def ajax_add_review(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST["review"],
        rating=request.POST["rating"],
    )

    context = {
        "user": user.username,
        "review": request.POST["review"],
        "rating": request.POST["rating"]
    }
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse({
        "bool": True,
        "context": context,
        "average_reviews": average_reviews['rating']  # Access the 'rating' value from the dict
    })
    
    

def search_view(request):
    query = request.GET.get("q", "")  # Use .get() to avoid KeyError if 'q' is missing
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    
    context = {
        "products": products,
        "query":query
    }
    
    return render(request, "core/search.html", context)


def filter_products(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')
    products = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
       products = products.filter(category__id__in=categories).distinct()
    if len(vendors) > 0:
         products = products.filter(vendor__id__in = vendors).distinct()
 
    n = render_to_string('core/async/product-list.html', {'products':products})
    return JsonResponse({'data' : n})



def add_to_cart(request):
    # del request.session['cartdata']
    cart_p = {}
    cart_p[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price']
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_p)
            request.session['cart_data_obj'] = cart_data
        else:
          cart_data = request.session['cart_data_obj']
          cart_data.update(cart_p)
          request.session['cart_data_obj'] = cart_data
    else:
      request.session['cart_data_obj'] = cart_p
      cart_data.update(cart_p)
      
        
    return JsonResponse({'data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

    
