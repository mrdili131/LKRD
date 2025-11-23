from django.urls import path
from .import views

urlpatterns = [
    path('',views.IndexView.as_view(),name='home'),
    path('transactions/',views.TransactionsView.as_view(),name='transactions'),
    path('settings/',views.SettingsView.as_view(),name='settings'),
    path('transfer/',views.TransferView.as_view(),name='transfer'),
    path('cheque/<int:id>/',views.ChequeView.as_view(),name='cheque'),
    path('cards/',views.CardsView.as_view(),name='cards'),
    path('edit_card/<int:id>/',views.EditCardView.as_view(),name='edit_card'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('get_loan/',views.GetLoanView.as_view(),name='get_loan'),
    path('notifications/',views.NotificationsView.as_view(),name='notifications'),
]