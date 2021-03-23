from django.urls import path, include
from logistics.views import *


purchase_url = [
	path('update/<int:pk>/', WorkPurchaseUpdate.as_view(), name="work-purchase-update"),
	path('create/<int:pk>/', WorkPurchaseCreate.as_view(), name="work-purchase-create"),
	path('delete/<int:pk>/', WorkPurchaseDeleteView.as_view(), name="work-purchase-delete"),
	path('list/', WorkPurchaseList.as_view(), name="work-purchase-list"),

	path('upload/update/<int:pk>/', UploadPurchaseUpdate.as_view(), name="upload-purchase-update"),
	path('upload/list/', UploadPurchaseList.as_view(), name="upload-purchase-list"),

	path('path/list/', OnPathPurchaseList.as_view(), name="path-purchase-list"),
	path('path/update/<int:pk>/', OnPathPurchaseUpdate.as_view(), name="path-purchase-update"),

	path('click/<int:pk>/', ClickPurchaseDetail.as_view(), name="city-click-purchase"),
	# path('click/update/<int:pk>/', ClickPurchaseUpdate.as_view(), name="click-purchase-update"),
	path('click/list/', ClickPurchaseList.as_view(), name="click-purchase-list"),

	path('status-list/', StatusPurchaseList.as_view(), name="status-purchase-list"),

	path('all-data/', all_data_purchase, name="all_data_purshase"),
	path('ajax_table_purchase/', ajax_table_purchase, name="ajax_table_purchase"),

	path('city/<int:pk>/', ajax_click_purchase, name="ajax_click_purchase"),
	path('city-load/<int:pk>/', ajax_purchase, name="ajax_purchase"),

]

sale_url = [
	path('update/<int:pk>/', WorkSaleUpdate.as_view(), name="work-sale-update"),
	path('create/<int:pk>/', WorkSaleCreate.as_view(), name="work-sale-create"),
	path('delete/<int:pk>/', WorkSaleDeleteView.as_view(), name="work-sale-delete"),
	path('list/', WorkSaleList.as_view(), name="work-sale-list"),

	path('upload/update/<int:pk>/', UploadSaleUpdate.as_view(), name="upload-sale-update"),
	path('upload/list/', UploadSaleList.as_view(), name="upload-sale-list"),

	path('path/list/', OnPathSaleList.as_view(), name="path-sale-list"),
	path('path/update/<int:pk>/', OnPathSaleUpdate.as_view(), name="path-sale-update"),

	path('click/<int:pk>/', ClickSaleDetail.as_view(), name="city-click-sale"),
	# path('click/update/<int:pk>/', ClickSaleUpdate.as_view(), name="click-sale-update"),
	path('click/list/', ClickSaleList.as_view(), name="click-sale-list"),

	path('status-list/', StatusSaleList.as_view(), name="status-sale-list"),
	path('all-data/', all_data_sale, name="all_data_sale"),
	path('ajax_table_sale/', ajax_table_sale, name="ajax_table_sale"),
	path('city/<int:pk>/', ajax_click_sale, name="ajax_click_sale"),
	path('city-load/<int:pk>/', ajax_sale, name="ajax_sale"),
]

urlpatterns = [
	path('purchase/', include(purchase_url)),
	path('sale/', include(sale_url)),
	# path('csv-response/', unruly_passengers_csv,)
]
