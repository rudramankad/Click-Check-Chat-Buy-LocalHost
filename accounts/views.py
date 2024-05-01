from django.shortcuts import render, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
import random
import string
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

def Click_Check_Chat_BuyLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('index:index')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('accounts:Click_Check_Chat_BuyLogin')
        
    else:
        return render(request, 'Click_Check_Chat_BuyLogin.html')



def Click_Check_Chat_BuyRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.save()
            messages.success(request, 'You have successfully registered.')
            return redirect('accounts:Click_Check_Chat_BuyLogin')
        except IntegrityError:
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'Click_Check_Chat_BuyRegister.html')
    else:
        return render(request, 'Click_Check_Chat_BuyRegister.html')

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user:
                characters = string.ascii_letters + string.digits + string.punctuation
                new_password = ''.join(random.choice(characters) for i in range(10))
                # Update user's password
                user.set_password(new_password)
                user.save()
                # Send email with reset password link
                send_mail(
                    'Reset Password mail from Click Check Chat Buy',
                    f'Dear {user.username},\nNow Your New Password is:  {new_password}',
                    'rudra15041998@gmail.com',  # TODO: Update this with your email id
                    [email],  # TODO: Update this with the recipient's email id
                    fail_silently=False,
                )
                messages.success(request, 'New password is sent to your registered email id.')
                return redirect('accounts:Click_Check_Chat_BuyLogin')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email. The email is not registered.')
            return render(request, 'forgotpassword.html')
    else:
        return render(request, 'forgotpassword.html')
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('index:index')