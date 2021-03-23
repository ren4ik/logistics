from django.urls import path

from .views import *

urlpatterns = [
	path('list/', SaleListView.as_view(), name="sale-bid-list"),
	path('<int:pk>/', SaleDetailView.as_view(), name="sale-bid"),
	path('create/', SaleCreateView.as_view(), name="sale-bid-create"),
	path('update/<int:pk>/', SaleUpdateView.as_view(), name="sale-bid-update"),
	path('delete/<int:pk>/', SaleDeleteView.as_view(), name="sale-bid-delete")
]
