from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

User = settings.AUTH_USER_MODEL

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    money = models.BigIntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return str(self.created_at)
