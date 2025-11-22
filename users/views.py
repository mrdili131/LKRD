from django.shortcuts import render, redirect
from .forms import LoginForm
from django.views import View
from django.contrib.auth import authenticate, login, logout


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
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                return redirect('auth:login')
        return render(request,"login.html",{"form":form})



def logoutview(request):
    logout(request)
    return redirect("home")