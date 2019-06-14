from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    TEMPLATE_HOME = 'home.html'
    return render(request, TEMPLATE_HOME)

def contact(request):
    TEMPLATE_CONTACT = 'contact.html'
    return render(request, TEMPLATE_CONTACT)