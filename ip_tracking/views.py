from django.shortcuts import render
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', block=True)
def public_view(request):
    return HttpResponse("Welcome public user!")


@ratelimit(key='user', rate='10/m', block=True)
def login_view(request):
    return HttpResponse("Login endpoint OK")
