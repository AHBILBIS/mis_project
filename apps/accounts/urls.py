from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manager-panel/', views.manager_only_view, name='manager_panel'),
    
    # REST API Token Exchange Endpoint
    path('api/api-token-auth/', obtain_auth_token, name='api_token_auth'),
]