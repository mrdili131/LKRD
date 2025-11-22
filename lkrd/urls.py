from django.urls import path
from .import views

urlpatterns = [
    path('',views.IndexView.as_view(),name='home'),
    path('transactions/',views.TransactionsView.as_view(),name='transactions'),
    path('settings/',views.SettingsView.as_view(),name='settings'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('get_loan/',views.GetLoanView.as_view(),name='get_loan'),
    path('notifications/',views.NotificationsView.as_view(),name='notifications'),
]