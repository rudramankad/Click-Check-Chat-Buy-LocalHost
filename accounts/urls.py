app_name = 'accounts'
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Click_Check_Chat_BuyLogin, name='Click_Check_Chat_BuyLogin'),
    path('register/', views.Click_Check_Chat_BuyRegister, name='Click_Check_Chat_BuyRegister'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('logout/', views.user_logout, name='user_logout'),
]
