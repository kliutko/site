from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Article
# Create your views here.
def index(request):
    return HttpResponse("Hello from the shop app+")