from django.urls import path
from .views import *


urlpatterns = [
	path('out-path/', OutPathList.as_view(), name="out-path"),
	path('out-path/<int:pk>/', OutSort.as_view(), name="out-path-sort"),
	path('out-path-response/', out_response,),

	path('in-path/', InPathList.as_view(), name="in-path"),
	path('in-path/<int:pk>/', InSort.as_view(), name="in-path-sort"),
	path('in-path-response/', in_response,),

	path('city/', CityList.as_view(), name="city"),
	path('client/', ClientList.as_view(), name="client_list"),
	path('provider/', ProviderList.as_view(), name="provider"),
	path('status/', StatusList.as_view(), name="status"),
	path('cargo/', CargoList.as_view(), name="cargo"),
	path('trade-term/', TradeTermList.as_view(), name="trade-term"),
	path('transport/', TransportList.as_view(), name="transport"),
	path('currency/', CurrencyList.as_view(), name="currency"),
	path('path/', PathList.as_view(), name="path"),
	path('logistics-provider/', LogisticsProviderList.as_view(), name="logistics-provider"),

	path('edit/', ajax_data,)
]
