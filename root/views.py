from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def home(request):
    template = 'root/home.html'
    context = {
        'title'     : 'IPPI',
        'page_name' : 'home',
        }
    return render(request, template, context)

def about(request):
    template = 'root/about.html'
    context = {
        'title'     : 'About IPPI',
        'page_name' : 'about',
        }
    return render(request, template, context)

