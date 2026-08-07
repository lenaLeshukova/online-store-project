from django.urls import path
from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    # Точный URL
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
]
