from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
import urllib.request
import requests
from django.contrib import auth
import os
from django.contrib.auth.models import User
from .models import extendeduser
# Create your views here.
def home(request):
    return render(request, 'accounts/basic.html')
def Farmer(request):
    return render(request, 'accounts/FarmerPage.html')
def Admin(request):
    return render(request, 'accounts/AdminPage.html')


def handlelogin(request):
    if request.method == "POST":
        uname1 = request.POST['uname1']
        pass3 = request.POST['pass3']
        user = auth.authenticate(username=uname1, password=pass3)
        if user is not None:
            auth.login(request, user)
            datas = extendeduser.objects.filter(user=request.user)
            messages.success(request, "Successfully logged in")
            if request.user.is_superuser:
                return redirect("admin")
            data = str(datas[0].cat)
            if data == "Farmer":
                return redirect('farmer')
            # return render(request,'accounts/FarmerPage.html')
            elif data == "Admin":
                return redirect('admin')
            # return render(request, 'accounts/AdminPage.html')
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, 'accounts/basic.html')
    else:
        return HttpResponse('NOT allowed')
def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return render(request, 'accounts/basic.html')
def signup(request):
    try:
        if request.method == 'POST':
            uname = request.POST['uname']
            email = request.POST['email']
            fname = request.POST['fname']
            lname = request.POST['lname']
            phone = request.POST['phone']
            cat = request.POST['cat']
            town=request.POST['town']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            if len(uname)<6:
                messages.error(request, "Week Username")
                return render(request, 'accounts/basic.html')
            if pass1!=pass2:
                messages.error(request, "Passwords not Same")
                return render(request, 'accounts/basic.html')
            if len(pass1)<6:
                messages.error(request, "Password must be greater than 6 characters")
                return render(request, 'accounts/basic.html')
            user = User.objects.create_user(uname, email, pass1)
            user.first_name = fname
            user.last_name = lname
            user.save()
            newuser = extendeduser(phone=phone, cat=cat,town=town, user=user)
            newuser.save()
            messages.success(request, "Your FarmerFriend Account has been Created Successfully")
            return render(request, 'accounts/basic.html')
    except:
        messages.error(request, "User with this information already exists")
        return render(request, 'accounts/basic.html')