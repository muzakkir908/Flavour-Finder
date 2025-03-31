from django.contrib import admin
from .models import OTPVerification

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('email', 'purpose', 'created_at', 'is_used')
    search_fields = ('email',)
    list_filter = ('purpose', 'is_used')
