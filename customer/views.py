from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Customer, Visit
from business.models import Business
import datetime

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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("customer:login"))
    elif request.method == "POST":
        query = request.POST["query"]
        try:
            businesses = Business.objects.filter(name__icontains=query)
        except DoesNotExist:
            businesses = []
        return render(request, 'customer/search.html', {
            "businesses": businesses
        })
    else:
        businesses = Business.objects.all()
        return render(request, 'customer/search.html', {
            "businesses": businesses
        })

def view(request, key):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("customer:login"))
    else:
        business = Business.objects.get(pk=key)
        return render(request, 'customer/view.html', {
            "business_name": business.name,
            "max_customers": business.max_customers,
            "open": business.open
        })

def reccomendation(request, key):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("customer:login"))
    else:
        business = Business.objects.get(pk=key)
        pass

def reserve(request, key):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("customer:login"))
    elif request.method == "POST":
        business = Business.objects.get(pk=key)
        customer = Customer.objects.get(user=request.user)
        date = request.POST["date"]
        visit = Visit(customer=customer, business=business, date=date)
        visit.save()
        return render(request, 'customer/reserve.html', {
            "business_name": business.name,
            "business_id": business.id,
            "message": "Succesfully reserved spot!"
        })
    else:
        business = Business.objects.get(pk=key)
        return render(request, 'customer/reserve.html', {
            "business_name": business.name,
            "business_id": business.id
        })

def positive(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("customer:login"))
    else:
        Customer.objects.filter(user=request.user).update(test_status=1)
        return render(request, 'customer/positive.html')

def negative(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("customer:login"))
    else:
        Customer.objects.filter(user=request.user).update(test_status=2)
        return render(request, 'customer/negative.html')

def alerts(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("customer:login"))
    else:
        customer = Customer.objects.get(user=request.user)
        alerts = []
        for i in range(14):
            date = datetime.date.today() - datetime.timedelta(days=i)
            try:
                visits = Visit.objects.filter(date=date)
            except DoesNotExist:
                continue
            businessPos = set()
            businessYou = set()
            for visit in visits:
                if visit.customer == customer:
                    businessYou.add(visit.business)
                elif visit.customer.test_status == 1:
                    businessPos.add(visit.business)
            for business in businessYou:
                if business in businessPos:
                    alerts.append("You may have been near someone who tested positive for COVID - 19. We reccomend you quarantine until " + str(date + datetime.timedelta(days=14)) + ".")
        return render(request, 'customer/alerts.html', {
            "alerts": alerts
        })
