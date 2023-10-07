from django.shortcuts import render
from django.http import HttpResponse
from .customDecorator import admin_required

# Create your views here.
def index(request):
    return HttpResponse(f'{request.user.username} and {request.user.is_staff}')

def pageNotAccessible(request):
    return HttpResponse("<h1>Why here son?</h1>")