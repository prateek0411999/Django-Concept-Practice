from django.shortcuts import render,HttpResponse
#render is there for the templates

# Create your views here.
def index(request):
    context={
        "var1": "this is done"
    }
    return render(request, 'index.html',context)
def about(request):
    return render(request, 'home/index.html')

def contact(request):
    return HttpResponse("This is contact page")


def services(request):
    return HttpResponse("This is services page")

