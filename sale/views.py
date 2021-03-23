from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from logistics.models import StatusBidSale
from .forms import BidSaleForm
from .models import *


class SaleListView(PermissionRequiredMixin, ListView):
	model = BidSale
	paginate_by = 20
	template_name = 'sale/bidsale_list.html'
	permission_required = 'sale.view_bidsale'
	login_url = 'login'
	ordering = ['-id']


class SaleDetailView(PermissionRequiredMixin, DetailView):
	model = BidSale
	template_name = 'sale/bidsale_detail.html'
	permission_required = 'sale.view_bidsale'
	login_url = 'login'


class SaleCreateView(PermissionRequiredMixin, CreateView):
	model = BidSale
	form_class = BidSaleForm
	template_name = 'sale/bidsale_create.html'
	success_url = reverse_lazy('sale-bid-list')
	permission_required = 'sale.view_bidsale'
	login_url = 'login'

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		StatusBidSale.objects.create(bid_id=form.save().id)
		return super(SaleCreateView, self).form_valid(form)


class SaleUpdateView(PermissionRequiredMixin, UpdateView):
	model = BidSale
	form_class = BidSaleForm
	success_url = reverse_lazy('sale-bid-list')
	template_name = 'sale/bidsale_update.html'
	permission_required = 'sale.add_bidsale'
	login_url = 'login'


class SaleDeleteView(PermissionRequiredMixin, DeleteView):
	model = BidSale
	success_url = reverse_lazy('sale-bid-list')
	template_name = 'sale/bidsale_delete.html'
	permission_required = 'sale.delete_bidsale'
	login_url = 'login'

	def delete(self, request, *args, **kwargs):
		"""
		Call the delete() method on the fetched object and then redirect to the
		success URL.
		"""
		self.object = self.get_object()
		success_url = self.get_success_url()
		info = f"{self.object.bid_number} {self.request.user}"
		SaleDelete.objects.create(info=info)
		self.object.delete()
		return HttpResponseRedirect(success_url)

