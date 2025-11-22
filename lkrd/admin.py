from django.contrib import admin
from .models import Transaction, Notification, Loan

admin.site.register([Transaction, Notification, Loan])