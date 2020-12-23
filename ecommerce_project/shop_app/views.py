from django.shortcuts import render
from django.views.generic import ListView, DetailView
from shop_app.models import *
#for login required
from django.contrib.auth.mixins import  LoginRequiredMixin
# Create your views here.
class Home(ListView):
    context_object_name = 'products'
    model = Product
    template_name = 'shop_app/home.html'

class ProductDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'product_details'
    model = Product
    template_name = 'shop_app/product_detail.html'
