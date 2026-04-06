from django.urls import path
from portal.views.auth_views import LoginView, LogoutView, MeView
from portal.views.record_views import RecordListCreateView, RecordDetailView
from portal.views.frontend_views import LoginPageView, DashboardPageView

urlpatterns = [
    path('', LoginPageView.as_view(), name='login_page'),
    path('dashboard/', DashboardPageView.as_view(), name='dashboard_page'),
    path('auth/login', LoginView.as_view(), name='auth_login'),
    path('auth/logout', LogoutView.as_view(), name='auth_logout'),
    path('users/me', MeView.as_view(), name='users_me'),
    path('records', RecordListCreateView.as_view(), name='record_list_create'),
    path('records/<uuid:pk>', RecordDetailView.as_view(), name='record_detail'),
]
