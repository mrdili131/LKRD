from django.db import models, transaction
from users.models import User
import uuid
from django.utils import timezone

transaction_status = (
    ("Success","Success"),
    ("Rejected","Rejected"),
    ("Cancelled","Cancelled"),
    ("Pending","Pending")
)

notification_type = (
    ("Ordinary","Ordinary"),
    ("Warning","Warning"),
)

class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    text = models.CharField(max_length=200)
    n_type = models.CharField(max_length=20,choices=notification_type,default="Ordinary")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Transaction(models.Model):
    sender = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='my_transactions')
    receiver = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    status = models.CharField(max_length=20,choices=transaction_status,default="Pending")
    amount = models.DecimalField(default=0,max_digits=20,decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        print("[LOGGER] Transaction is being created")
        is_new = self._state.adding

        if is_new and self.sender and self.receiver:
            with transaction.atomic():
                sender = User.objects.select_for_update().get(id=self.sender.id)
                receiver = User.objects.select_for_update().get(id=self.receiver.id)
                if (self.amount <= sender.balance):
                    sender.balance -= self.amount
                    receiver.balance += self.amount
                    sender.save()
                    receiver.save()
                    Notification(user=sender,text=f'Siz {receiver.full_name} ga {self.amount} so\'m jo\'natdingiz',n_type='Ordinary').save()
                    Notification(user=receiver,text=f'Sizning balansingizga {sender.full_name} tomonidan {self.amount} so\'m qabul qilindi',n_type='Ordinary').save()
                    self.status = "Success"
                    print("[LOGGER] Transaction succeed")
                else:
                    self.status = "Rejected"
                    print("[LOGGER] Transaction rejected")
        print("[LOGGER] Transaction is saved")
        super().save(*args,**kwargs)

    def __str__(self):
        return f'From: {self.sender.username} to: {self.receiver.username} amount: {self.amount} status: {self.status}'


class Loan(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.DecimalField(default=0,max_digits=20,decimal_places=0)
    is_signed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    month_length = models.IntegerField(default=12)
    pay_day = models.DateField(default=timezone.now)
    accepted_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        Notification(user=self.user,text=f"{self.amount} so'm summani {self.month_length} muddatiga kredit olish uchun buyurtma berdingiz. Buyurtma tasdiqlanish jarayonida.",n_type='Ordinary').save()
        super().save(*args,**kwargs)

    def __str__(self):
        return f'{self.user.full_name} | {self.amount} so\'m | {self.month_length} oy | {self.created_at.ctime()} da | status: {self.is_active}'

