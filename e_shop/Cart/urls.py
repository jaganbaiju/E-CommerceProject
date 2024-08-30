from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('cart_details', views.cart_details, name='cart_details'),
    path('add/<int:p_id>/', views.add_cart, name='add_cart'),
    path('remove/<int:p_id>/', views.cart_remove, name='cart_remove'),
    path('delete/<int:p_id>/', views.cart_delete, name='cart_delete'),

]
