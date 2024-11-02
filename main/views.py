from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def learn(request):
    return render(request, 'learn.html')

def contact(request):
    return render(request, 'contact.html')