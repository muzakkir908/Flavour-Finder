import requests
import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from .forms import (
    UserLoginForm, UserRegistrationForm, RequestPasswordResetForm, 
    VerifyOTPForm, SetNewPasswordForm
)
from .models import OTPVerification

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                # Redirect to the page the user was trying to access, or home
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def request_password_reset(request):
    if request.method == 'POST':
        form = RequestPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            
            # Check if user exists with this email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'No account found with that email.')
                return redirect('request_password_reset')
            
            # Call the OTP service API
            try:
                response = requests.post(
                    settings.OTP_SERVICE_URL,
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps({
                        'email': email,
                        'purpose': 'password reset'
                    })
                )
                
                data = response.json()
                
                if data.get('success'):
                    # Store OTP in the database
                    OTPVerification.objects.create(
                        user=user,
                        email=email,
                        otp=data.get('otp'),
                        purpose='password_reset'
                    )
                    
                    messages.success(request, 'OTP sent to your email. Please check your inbox.')
                    return redirect('verify_otp', email=email)
                else:
                    messages.error(request, f"Error: {data.get('message')}")
            except Exception as e:
                messages.error(request, f"Error connecting to OTP service: {str(e)}")
    else:
        form = RequestPasswordResetForm()
    
    return render(request, 'accounts/request_password_reset.html', {'form': form})

def verify_otp(request, email):
    if request.method == 'POST':
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            
            # Verify OTP
            verification = OTPVerification.objects.filter(
                email=email,
                otp=otp,
                is_used=False,
                purpose='password_reset'
            ).order_by('-created_at').first()
            
            if verification and verification.is_valid():
                # Mark OTP as used
                verification.is_used = True
                verification.save()
                
                messages.success(request, 'OTP verified successfully. Set your new password.')
                return redirect('set_new_password', email=email, otp=otp)
            else:
                messages.error(request, 'Invalid or expired OTP. Please try again.')
    else:
        form = VerifyOTPForm()
    
    return render(request, 'accounts/verify_otp.html', {'form': form, 'email': email})

def set_new_password(request, email, otp):
    # Verify OTP one more time to ensure security
    verification = OTPVerification.objects.filter(
        email=email,
        otp=otp,
        is_used=True,
        purpose='password_reset'
    ).order_by('-created_at').first()
    
    if not verification:
        messages.error(request, 'Invalid verification token.')
        return redirect('request_password_reset')
    
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=email)
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                
                messages.success(request, 'Password has been reset successfully. You can now login with your new password.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
                return redirect('request_password_reset')
    else:
        form = SetNewPasswordForm()
    
    return render(request, 'accounts/set_new_password.html', {'form': form})
