from django.db import models

class Transaction(models.Model):
    name = models.CharField(max_length=100) 
    email = models.EmailField(max_length=100) 
    checkout_id = models.CharField(max_length=100, unique=True)
    mpesa_code = models.CharField(max_length=100, null=True, blank=True) 
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mpesa_code} - {self.status}"
