from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate

def index(request):
    return render_to_response('index.html')

def profile(request):
    user = request.POST.get('username')
    data = { 'user': user }
    return render_to_response('index.html', data)