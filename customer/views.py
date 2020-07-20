from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("customer:login"))
    return HttpResponse("hello")

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
        pass
    else:
        return HttpResponseRedirect("customer:login")

def signup_view(request):
    pass

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
