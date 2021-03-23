from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse, response
from django.views.generic.base import View

from .forms import *
from .utils import *

from handbook.models import *


class OutPathList(PermissionRequiredMixin, ObjectDetailMixin2, View):
	"""получение списка, CRUD - OutPath"""
	model = OutPath
	template_name = 'handbook/path-list.html'
	url = "/handbook/out-path/"
	form_name = OutPathForm
	permission_required = 'handbook.add_outpath'
	login_url = 'login'


class InPathList(PermissionRequiredMixin, ObjectDetailMixin2, View):
	"""получение списка, CRUD - InPath"""
	model = InPath
	template_name = 'handbook/path-list.html'
	url = "/handbook/in-path/"
	form_name = InPathForm
	permission_required = 'handbook.add_inpath'
	login_url = 'login'


class InSort(PermissionRequiredMixin, ObjectDetailMixin3, View):
	"""получение списка, CRUD - InPath"""
	model = InPathSort
	extra_model = InPath
	template_name = 'handbook/path-sort.html'
	url = "/handbook/in-path-response/"
	permission_required = 'handbook.add_inpathsort'
	login_url = 'login'


class OutSort(PermissionRequiredMixin, ObjectDetailMixin3, View):
	"""получение списка, CRUD - InPath"""
	model = OutPathSort
	extra_model = OutPath
	template_name = 'handbook/path-sort.html'
	url = "/handbook/out-path-response/"
	permission_required = 'handbook.add_outpathsort'
	login_url = 'login'


@permission_required('handbook.add_outpath', login_url='/login/')
def out_response(request):
	pk = request.session['path_id']
	obj = OutPath.objects.get(pk=pk)
	url = obj.get_absolute_url
	template_name = 'handbook/response.html'
	city_list = OutPathSort.objects.filter(path_code=pk)
	city = city_list.exists()

	return render(request, template_name, {
		'obj': obj,
		"city_list": city_list,
		"city": city,
		"url": url
	})


@permission_required('handbook.add_inpath', login_url='/login/')
def in_response(request):
	pk = request.session['path_id']
	obj = InPath.objects.get(pk=pk)
	url = obj.get_absolute_url
	template_name = 'handbook/response.html'
	city_list = InPathSort.objects.filter(path_code=pk)
	city = city_list.exists()

	return render(request, template_name, {
		'obj': obj,
		"city_list": city_list,
		"city": city,
		"url": url
	})


class CityList(PermissionRequiredMixin, ObjectDetailMixin, View):
	"""получение списка, CRUD - city"""
	model = City
	template_name = 'handbook/list.html'
	url = "/handbook/city/"
	permission_required = 'handbook.add_city'
	login_url = 'login'


class ClientList(PermissionRequiredMixin, ObjectDetailMixin, View):
	"""получение списка, CRUD - Client"""
	model = Client
	template_name = 'handbook/list.html'
	url = "/handbook/client/"
	permission_required = 'handbook.add_client'
	login_url = 'login'


class ProviderList(PermissionRequiredMixin, ObjectDetailMixin, View):
	"""получение списка, CRUD - provider"""
	model = Provider
	template_name = 'handbook/list.html'
	url = "/handbook/provider/"
	permission_required = 'handbook.add_provider'
	login_url = 'login'


class CargoList(PermissionRequiredMixin, ObjectDetailMixin, View):
	"""получение списка, CRUD - cargo"""
	model = Cargo
	template_name = 'handbook/list.html'
	url = "/handbook/cargo/"
	permission_required = 'handbook.add_cargo'
	login_url = 'login'


class TradeTermList(PermissionRequiredMixin, ObjectDetailMixin, View):
	"""получение списка, CRUD - TradeTerm"""
	model = TradeTerm
	template_name = 'handbook/list.html'
	url = "/handbook/trade-term/"
	permission_required = 'handbook.add_tradeterm'
	login_url = 'login'


class StatusList(PermissionRequiredMixin, ObjectDetailMixin, View):
	"""получение списка, CRUD - status"""
	model = Status
	template_name = 'handbook/list.html'
	url = "/handbook/status/"
	permission_required = 'handbook.add_status'
	login_url = 'login'


class TransportList(PermissionRequiredMixin, ObjectDetailMixin, View):
	"""получение списка, CRUD - transport"""
	model = Transport
	template_name = 'handbook/list.html'
	url = "/handbook/transport/"
	permission_required = 'handbook.add_transport'
	login_url = 'login'


class CurrencyList(PermissionRequiredMixin, ObjectDetailMixin, View):
	"""получение списка, CRUD - Currency"""
	model = Currency
	template_name = 'handbook/list.html'
	url = "/handbook/currency/"
	permission_required = 'handbook.add_currency'
	login_url = 'login'


class PathList(PermissionRequiredMixin, ObjectDetailMixin, View):
	"""получение списка, CRUD - Path"""
	model = Path
	template_name = 'handbook/list.html'
	url = "/handbook/path/"
	permission_required = 'handbook.add_path'
	login_url = 'login'


class LogisticsProviderList(PermissionRequiredMixin, ObjectDetailMixin, View):
	"""получение списка, CRUD - Provider"""
	model = LogisticsProvider
	template_name = 'handbook/list.html'
	url = "/handbook/logistics-provider/"
	permission_required = 'handbook.view_cargo'
	login_url = 'login'


def ajax_data(request):
	if request.is_ajax():
		if request.GET.get('name') == 'inpath':
			req1 = InPathSort.objects.get(id=request.GET.get('id'))
			if request.GET.get('id') and request.GET.get('sort'):
				req1.sort = request.GET.get('sort')
				req1.save(update_fields=['sort'])
			elif request.GET.get('id') and request.GET.get('transport'):
				req1.transport_id = request.GET.get('transport')
				req1.save(update_fields=['transport'])
		else:
			req2 = OutPathSort.objects.get(id=request.GET.get('id'))
			if request.GET.get('id') and request.GET.get('sort'):
				req2.sort = request.GET.get('sort')
				req2.save(update_fields=['sort'])
			elif request.GET.get('id') and request.GET.get('transport'):
				req2.transport_id = request.GET.get('transport')
				req2.save(update_fields=['transport'])

		data = {
			'yes': True
		}
		return JsonResponse(data)


