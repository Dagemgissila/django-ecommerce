from django.shortcuts import render,redirect
from . forms import UserRegisterForm
from django.contrib.auth import login,authenticate ,logout
from django.contrib import messages
from django.conf import settings
from userauthes.models import User

# User = settings.AUTH_USER_MODEL
# Create your views here.

def register_view(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user=form.save()
            username=form.cleaned_data.get("username")
            messages.success(request,f"Hello {username} ,You account is created successfully")
            new_user=authenticate(username=form.cleaned_data["email"],password=form.cleaned_data["password1"])
            login(request,new_user)
            return redirect("core:index")
    else:
         form=UserRegisterForm()
         
    context={
        'form':form
    }
    return render(request,'userauthes/sign-up.html',context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
         
            if user is not None:
              login(request, user)
              messages.success(request, "You are logged in")
              return redirect("core:index")
            else:
             messages.warning(request, "Invalid credentials")
        except:
            messages.warning(request, f"User with email {email} is not found")
            return render(request, "userauthes/sign-in.html")
    else:
        return render(request, "userauthes/sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request,"You logged out")
    return redirect("userauthes:sign-in")
        
