from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Customer

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("customer:login"))
    else:
        customer = Customer.objects.get(user=request.user)
        return render(request, "customer/customer.html", {
            "test_status": customer.test_status
        })

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("customer:customer"))
    elif request.method == "POST":
        username = request.POST["username"]
        password = request. POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("customer:customer"))
        else:
            return render(request, "customer/login.html", {
                "message": "Wrong username or password."
            })
    else:
        return render(request, "customer/login.html")

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, "customer/login.html", {
            "message": "Logged out succesfully."
        })
    else:
        return HttpResponseRedirect("customer:login")

def signup_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("customer:customer"))
    elif request.method == "POST":
        username = request.POST["username"]
        password = request. POST["password"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]

        if User.objects.filter(username=username).exists():
            return render(request, "customer/signup.html", {
                "message": "That username is already taken."
            })
        else:
            user = User.objects.create_user(username=username, password=password, first_name=firstname, last_name=lastname)
            user.save()
            customer = Customer(user=user, test_status=0, quarantined=0)
            customer.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("customer:customer"))
            else:
                return render(request, "customer/signup.html", {
                    "message": "Sorry, there was some error."
                })
    else:
        return render(request, "customer/signup.html")

def search(request):
    pass

def view(request):
    pass

def reccomendation(request):
    pass

def reserve(request):
    pass

def positive(request):
    pass

def negative(request):
    pass

def alerts(request):
    pass
