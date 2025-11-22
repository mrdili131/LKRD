from django.shortcuts import render, redirect
from .forms import LoginForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from lkrd.models import Notification


class LoginView(View):
    def get(self,request):
        form = LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            print("[LOGGER] Authenticating user")
            if user is not None:
                login(request,user)
                print("[LOGGER] Logged in")
                Notification(user=request.user,text='Akauntingizga kirish amalga oshirildi',n_type='Warning').save()
                return redirect('home')
            else:
                print("[LOGGER] Error in loggin in")
                return redirect('auth:login')
        return render(request,"login.html",{"form":form})



def logoutview(request):
    if request.user:
        Notification(user=request.user,text='Akauntingizga chiqish amalga oshirildi',n_type='Warning').save()
    logout(request)
    return redirect("home")