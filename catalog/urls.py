from django.urls import path
from catalog.views import (
    ProductListView, ContactsView, ProductDetailView,
    ProductCreateView, ProductUpdateView, ProductDeleteView
)
from catalog.views import TogglePublishView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(),
        name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:pk>/toggle-publish/', TogglePublishView.as_view(),
      name='toggle_publish'),
]
