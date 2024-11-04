import os, re, base64, json, requests
from datetime import datetime
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Transaction
from .forms import PaymentForm
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve variables from the environment
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")
MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE")
CALLBACK_URL = os.getenv("CALLBACK_URL")
MPESA_BASE_URL = os.getenv("MPESA_BASE_URL")

# Hardcoded amount
AMOUNT = 1  # Change this to your desired amount

# Phone number formatting and validation
def format_phone_number(phone):
    phone = phone.replace("+", "")
    if re.match(r"^254\d{9}$", phone):
        return phone
    elif phone.startswith("0") and len(phone) == 10:
        return "254" + phone[1:]
    else:
        raise ValueError("Invalid phone number format")

# Generate M-Pesa access token
def generate_access_token():
    try:
        credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
        }
        response = requests.get(
            f"{MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
            headers=headers,
        ).json()

        if "access_token" in response:
            return response["access_token"]
        else:
            raise Exception("Access token missing in response.")
    except requests.RequestException as e:
        raise Exception(f"Failed to connect to M-Pesa: {str(e)}")

# Initiate STK Push and handle response
def initiate_stk_push(phone):
    try:
        token = generate_access_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        stk_password = base64.b64encode(
            (MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).encode()
        ).decode()

        request_body = {
            "BusinessShortCode": MPESA_SHORTCODE,
            "Password": stk_password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": AMOUNT,
            "PartyA": phone,
            "PartyB": MPESA_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": CALLBACK_URL,
            "AccountReference": "account",
            "TransactionDesc": "Payment for goods",
        }

        response = requests.post(
            f"{MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest",
            json=request_body,
            headers=headers,
        ).json()

        return response
    except Exception as e:
        print(f"Failed to initiate STK Push: {str(e)}")
        return {"error": str(e)}
        
def learn(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                phone_number = format_phone_number(form.cleaned_data["phone_number"])

                response = initiate_stk_push(phone_number)
                print("STK Push Response:", response)  # Log response

                if response.get("ResponseCode") == "0":
                    print("STK push successful, preparing to render payment.html")
                    checkout_request_id = response["CheckoutRequestID"]
                    transaction = Transaction(
                        name=name,
                        email=email,
                        checkout_id=checkout_request_id,
                        phone_number=phone_number,
                        status='Pending'
                    )
                    transaction.save()
                    return render(request, "payment.html", {"checkout_request_id": checkout_request_id})
                else:
                    print("STK Push Failed")  # Log failure
                    error_message = response.get("errorMessage", "Failed to send STK push. Please try again.")
                    return render(request, "learn.html", {"form": form, "error_message": error_message})
            except ValueError as e:
                print("ValueError encountered:", e)
                return render(request, "learn.html", {"form": form, "error_message": str(e)})
            except Exception as e:
                print("Unexpected error:", e)
                return render(request, "learn.html", {"form": form, "error_message": f"An unexpected error occurred: {str(e)}"})
        else:
            error_message = "There was an error with your submission. Please check the form fields."
            return render(request, "learn.html", {"form": form, "error_message": error_message})
    else:
        form = PaymentForm()
    print("Rendering learn.html for GET request")
    return render(request, "learn.html", {"form": form})

# Query STK Push status
def query_stk_push(checkout_request_id):
    try:
        token = generate_access_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(
            (MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).encode()
        ).decode()

        request_body = {
            "BusinessShortCode": MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }

        response = requests.post(
            f"{MPESA_BASE_URL}/mpesa/stkpushquery/v1/query",
            json=request_body,
            headers=headers,
        )
        print(response.json())
        return response.json()
    except requests.RequestException as e:
        print(f"Error querying STK status: {str(e)}")
        return {"error": str(e)}

# View to query the STK status and return it to the frontend
def stk_status_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            checkout_request_id = data.get('checkout_request_id')
            print("CheckoutRequestID:", checkout_request_id)

            status = query_stk_push(checkout_request_id)
            return JsonResponse({"status": status})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt  
def payment_callback(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST requests are allowed")

    try:
        callback_data = json.loads(request.body)
        result_code = callback_data["Body"]["stkCallback"]["ResultCode"]
        checkout_id = callback_data["Body"]["stkCallback"]["CheckoutRequestID"]

     
        try:
            transaction = Transaction.objects.get(checkout_id=checkout_id)

            if result_code == 0:
             
                metadata = callback_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
                mpesa_code = next(item["Value"] for item in metadata if item["Name"] == "MpesaReceiptNumber")
                phone = next(item["Value"] for item in metadata if item["Name"] == "PhoneNumber")

              
                transaction.mpesa_code = mpesa_code
                transaction.phone_number = phone
                transaction.status = "Success"
                transaction.save()

                return JsonResponse({"ResultCode": 0, "ResultDesc": "Payment successful"})

            else:
                transaction.status = "Failed"
                transaction.save()
                return JsonResponse({"ResultCode": result_code, "ResultDesc": "Payment failed"})

        except Transaction.DoesNotExist:
            # Handle the case where the transaction is not found
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Transaction not found"}, status=404)

    except (json.JSONDecodeError, KeyError) as e:
        return HttpResponseBadRequest(f"Invalid request data: {str(e)}")

def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')
