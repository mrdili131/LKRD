from django.contrib import admin
from .models import Transaction, Notification, Loan, Card, News

admin.site.register([Transaction, Notification, Loan, Card, News])