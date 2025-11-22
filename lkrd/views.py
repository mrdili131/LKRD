from django.shortcuts import render
from django.views import View
from .models import Transaction, Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.utils import timezone

class IndexView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'index.html')

class TransactionsView(LoginRequiredMixin,View):
    def get(self,request):
        now = timezone.now()
        transactions = Transaction.objects.filter(Q(sender=request.user)|Q(receiver=request.user)).order_by("-created_at")
        monthly_spending_obj = Transaction.objects.filter(
            created_at__year=now.year,
            created_at__month=now.month,
            sender=request.user
        )
        monthly_income_obj = Transaction.objects.filter(
            created_at__year=now.year,
            created_at__month=now.month,
            receiver=request.user
        )
        spending = monthly_spending_obj.aggregate(total=Sum('amount'))['total'] or 0
        income = monthly_income_obj.aggregate(total=Sum('amount'))['total'] or 0
        return render(request,'transactions.html',{"transactions":transactions,"spending":spending,"income":income})

class SettingsView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'settings.html')

class ProfileView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'edit-profile.html')

class NotificationsView(LoginRequiredMixin,View):
    def get(self,request):
        notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
        return render(request,'notifications.html',{"notifications":notifications})

class GetLoanView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'loan.html')