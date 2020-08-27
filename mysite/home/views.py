from django.shortcuts import render,HttpResponse
#render is there for the templates

# Create your views here.
def index(request):
    return HttpResponse("This is homepage")

def about(request):
    return HttpResponse("This is about page")


def contact(request):
    return HttpResponse("This is contact page")


def services(request):
    return HttpResponse("This is services page")

