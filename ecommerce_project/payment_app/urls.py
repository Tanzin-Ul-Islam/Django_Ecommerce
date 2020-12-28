from django.urls import path
from payment_app import views
app_name = 'payment_app'
urlpatterns =[
    path('checkout/', views.checkout, name='checkout'),
    path('proceed/', views.payment, name="proceed"),
    path('payment_status/', views.payment_status, name="payment_status")
]