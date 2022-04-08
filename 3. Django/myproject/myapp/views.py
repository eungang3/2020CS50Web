from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def greet(request, name):
    return render(request, "myapp/index.html", {
        "name": name.capitalize()
    })
