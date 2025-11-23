from django.shortcuts import render, redirect
from django.views import View
from .models import Transaction, Notification, Card, News
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.utils import timezone
from .forms import TransactionForm

class IndexView(LoginRequiredMixin,View):
    def get(self,request):
        balance = Card.objects.filter(user=request.user).aggregate(total=Sum('balance'))['total'] or 0
        news = News.objects.all().order_by("-created_at")
        return render(request,'index.html',{"balance":balance,"news":news})

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

class TransferView(LoginRequiredMixin,View):
    def get(self,request):
        form = TransactionForm()
        return render(request,'transfer.html',{"form":form})
    def post(self,request):
        form = TransactionForm(request.POST)
        print(form.errors)
        if form.is_valid():
            sender_card = Card.objects.get(number=form.cleaned_data["sender_card"])
            receiver_card = Card.objects.get(number=form.cleaned_data["receiver_card"])
            Transaction(
                sender = request.user,
                receiver = receiver_card.user,
                sender_card = sender_card,
                receiver_card = receiver_card,
                status = "Pending",
                amount = form.cleaned_data["amount"]
            ).save()
            redirect('transactions')
        return render(request,'transfer.html',{"form":form})
    
class ChequeView(View):
    def get(self,request,id):
        transaction = Transaction.objects.get(id=id)
        return render(request,'cheque.html',{"transaction":transaction})

class CardsView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'cards.html')
    
class EditCardView(LoginRequiredMixin,View):
    def get(self,request,id):
        card = Card.objects.get(id=id)
        if card.user == request.user:
            return render(request,'edit-card.html',{"card":card})
        else:
            return redirect("home")

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