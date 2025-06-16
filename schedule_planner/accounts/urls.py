from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.accounts_index, name="accounts_index"),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('authenticate_user/', views.authenticate_user,
         name='authenticate_user'),
    path('logout', views.logout_view, name='logout')
]
