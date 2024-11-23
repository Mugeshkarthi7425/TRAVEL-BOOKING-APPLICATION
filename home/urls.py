from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('service/', views.service, name='service'),
    path('booking', views.booking, name="booking"),
    path('login/', views.login, name='login'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('logout', views.handlelogout, name="logout"),
    path('register', views.register, name="register"),
    path('Return', views.Return, name="Return"),
    path('oneway', views.oneway, name="oneway"),
    path('adminpage',views.adminpage, name= "adminpage"),
    path('addflight',views.addflight, name= "addflight"),
    path('ticketdetails',views.ticketdetails, name= "ticketdetails"),
    path('savepassenger',views.savepassenger,name="savepassenger"),
    path('payment',views.payment,name="payment"), 
    path('payment-success/', views.payment_success, name='payment_success'), 
    path('logout/', views.handlelogout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('editflight/<int:id>/', views.edit_flight, name='edit_flight'),
    path('deleteflight/<int:id>/', views.delete_flight, name='delete_flight'),
]

