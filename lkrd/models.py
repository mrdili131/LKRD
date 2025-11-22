from django.db import models
from users.models import User

class Transaction(models.Model):
    sender = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='my_transactions')
    receiver = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    amount = models.DecimalField(default=0,max_digits=20,decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From: {self.sender.username} to: {self.receiver.username} amount: {self.amount}'