from django.urls import path
from order_app import views

app_name = "order_app"

urlpatterns = [
    path('add/<pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove_item/<pk>/', views.remove_cart_item, name="remove_cart_item"),
    path('increase_quantity/<pk>/', views.increase_item_quantity, name="increase"),
    path('decrease_quantity/<pk>/', views.decrease_item_quantity, name="decrease"),
]