from django.shortcuts import render, HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def projects(request):
    return render(request, 'project.html')

def services(request):
    return render(request, 'services.html')

def team(request):
    return render(request, 'team.html')

def blog(request):
    return render(request, 'blog.html')

def contact(request):
    return render(request, 'contact.html')

def blankpage(request):
    return render(request, '404.html')


def send_email_view(request):
    if request.method == 'POST':
        name = request.POST.get('your_name')
        email = request.POST.get('your_email')
        subject = request.POST.get('subject')
        visitor_message = request.POST.get('message')

        # Customize the message content
        your_custom_message = f"Name: {name}\nSubject: {subject}\nFrom: {email}\nVisitor Message:\n{visitor_message}"

        try:
            email_sending_successful = send_mail(
                f"Feedback Form: {subject}",
                your_custom_message,
                'janjaprogrammers@gmail.com',
                ['janjaprogrammers@gmail.com'],
                fail_silently=False,
            )
        except Exception as e:
            email_sending_successful = False

            if email_sending_successful:
                return HttpResponseRedirect(reverse('contact'))
            else:
                raise ConnectionRefusedError(e)
    
    return render(request, 'contact.html')




def request_payment(request):
    if request.method == 'POST':
        name = request.POST.get('your_name')
        email = request.POST.get('your_email')
        phone = request.POST.get('phone')

        # Customize the message content
        your_custom_message = f"Applicant's Name: {name}\n\nContact Details:\n\tEmail: {email}\n\tPhone:\n{phone}"

        try:
            send_mail(
                "PAYMENT REQUEST FORM",
                your_custom_message,
                'janjaprogrammers@gmail.com',
                ['janjaprogrammers@gmail.com'],
                fail_silently=False,
            )
            return JsonResponse({'message': 'Your request has been received. We will send the payment details to your provided contact information shortly.'})
        except Exception as e:
            return JsonResponse({'message': 'There was an error processing your request. Please try again.'}, status=500)

    # If not POST method, or any other issue
    return JsonResponse({'message': 'Invalid request method.'}, status=400)


def enroll(request):
    return render(request, 'enroll.html')

