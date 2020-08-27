from django.shortcuts import render,HttpResponse

# Create your views here.
def polls(request):
    return HttpResponse("this is polls page")