from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return HttpResponse("Market Safe!")
