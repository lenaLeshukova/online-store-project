from django.urls import path
from catalog.views import ProductListView, ContactsView, ProductDetailView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
