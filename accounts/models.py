from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    purpose = models.CharField(max_length=100, default='password_reset')
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.email} - {self.purpose}"
    
    def is_valid(self):
        # OTP expires after 10 minutes
        expiration_time = self.created_at + datetime.timedelta(minutes=10)
        return not self.is_used and timezone.now() <= expiration_time
