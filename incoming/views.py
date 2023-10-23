from django.shortcuts import render, HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def projects(request):
    return render(request, 'project.html')

def team(request):
    return render(request, 'team.html')

def contact(request):
    return render(request, 'contact.html')

def blankpage(request):
    return render(request, '404.html')


def send_email_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            email_sending_successful= send_mail(
            name,
            subject,
            message,
            email,
            ['janjaprogrammers@gmail.com'],
            fail_silently=False,
        )
        except Exception as e:
            email_sending_successful = False

            if email_sending_successful:
                return HttpResponseRedirect(reverse('contact'))
            else:
                return HttpResponseRedirect(reverse('blankpage'))
    return render(request, 'contact.html')

