from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Business
from customer.models  import Customer, Visit
import datetime

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("business:login"))
    else:
        business = Business.objects.get(user=request.user)
        return render(request, "business/business.html", {
            "open": business.open
        })

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("business:business"))
    elif request.method == "POST":
        username = request.POST["username"]
        password = request. POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("business:business"))
        else:
            return render(request, "business/login.html", {
                "message": "Wrong username or password."
            })
    else:
        return render(request, "business/login.html")

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, "business/login.html", {
            "message": "Logged out succesfully."
        })
    else:
        return HttpResponseRedirect("business:login")

def register_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("business:business"))
    elif request.method == "POST":
        username = request.POST["username"]
        password = request. POST["password"]
        name = request.POST["name"]
        max_customers = request.POST["max_customers"]
        avg_customers = request.POST["avg_customers"]
        employees = request.POST["employees"]
        area = request.POST["area"]

        if User.objects.filter(username=username).exists():
            return render(request, "business/register.html", {
                "message": "That username is already taken."
            })
        else:
            user = User.objects.create_user(username=username, password=password, first_name=name)
            user.save()
            business = Business(user=user, name=name, max_customers=max_customers, avg_customers=avg_customers, employees=employees, area=area, open=1)
            business.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("business:business"))
            else:
                return render(request, "business/register.html", {
                    "message": "Sorry, there was some error."
                })
    else:
        return render(request, "business/register.html")

def edit(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("business:login"))
    elif request.method == "POST":
        max_customers = request.POST["max_customers"]
        avg_customers = request.POST["avg_customers"]
        employees = request.POST["employees"]
        area = request.POST["area"]
        Business.objects.filter(user=request.user).update(max_customers=max_customers, avg_customers=avg_customers, employees=employees, area=area)
        return HttpResponseRedirect(reverse("business:analytics"))
    else:
        business = Business.objects.get(user=request.user)
        return render(request, "business/edit.html", {
            "max_customers": business.max_customers,
            "avg_customers": business.avg_customers,
            "employees": business.employees,
            "area": business.area
        })

def analytics(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("business:login"))
    else:
        business = Business.objects.get(user=request.user)
        return render(request, "business/analytics.html", {
            "max_customers": business.max_customers,
            "avg_customers": business.avg_customers,
            "employees": business.employees,
            "area": business.area
        })

def spots(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("business:login"))
    else:
        business = Business.objects.get(user=request.user)
        todays_date = datetime.date.today()
        tomorrows_date = todays_date + datetime.timedelta(days = 1)
        todays_visits = Visit.objects.filter(business=business, date=todays_date)
        tomorrows_visits = Visit.objects.filter(business=business, date=tomorrows_date)
        return render(request, 'business/spots.html', {
            "todays_visits": todays_visits,
            "tomorrows_visits": tomorrows_visits
        })

def positive(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("business:login"))
    else:
        Business.objects.filter(user=request.user).update(open=0)
        return render(request, 'business/positive.html')

def negative(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("business:login"))
    else:
        Business.objects.filter(user=request.user).update(open=1)
        return render(request, 'business/negative.html')

def alerts(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("customer:login"))
    else:
        business = Business.objects.get(user=request.user)
        alerts = []
        for i in range(14):
            date = datetime.date.today() - datetime.timedelta(days=i)
            try:
                visits = Visit.objects.filter(business=business, date=date)
            except DoesNotExist:
                continue
            for visit in visits:
                if visit.customer.test_status == 1:
                    alerts.append("You may have been near someone who tested positive for COVID - 19. We reccomend you quarantine until " + str(date + datetime.timedelta(days=14)) + ".")
        return render(request, 'business/alerts.html', {
            "alerts": alerts
        })
