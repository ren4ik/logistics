from django.urls import path

from purchase.views import *

urlpatterns = [
	path('list/', PurchaseListView.as_view(), name="purchase-bid-list"),
	path('<int:pk>/', PurchaseDetailView.as_view(), name="purchase-bid"),
	path('create/', PurchaseCreateView.as_view(), name="purchase-bid-create"),
	path('update/<int:pk>/', PurchaseUpdateView.as_view(), name="purchase-bid-update"),
	path('delete/<int:pk>/', PurchaseDeleteView.as_view(), name="purchase-bid-delete")
]
