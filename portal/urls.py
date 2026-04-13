from django.urls import path
from .views import LoginPageView, DashboardPageView, LogoutView, CreateRecordView

urlpatterns = [
    path('', LoginPageView.as_view(), name='login'),
    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('records/create/', CreateRecordView.as_view(), name='create_record'),
]
