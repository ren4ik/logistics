from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from logistics.models import StatusBidPurchase
from .forms import BidPurchaseForm
from .models import BidPurchase, PurchaseDelete


class PurchaseListView(PermissionRequiredMixin, ListView):
	model = BidPurchase
	paginate_by = 20
	template_name = 'purchase/purchase_list.html'
	permission_required = 'purchase.view_bidpurchase'
	login_url = 'login'
	ordering = ['-id']


class PurchaseDetailView(PermissionRequiredMixin, DetailView):
	model = BidPurchase
	template_name = 'purchase/purchase_detail.html'
	permission_required = 'purchase.view_bidpurchase'
	login_url = 'login'


class PurchaseCreateView(PermissionRequiredMixin, CreateView):
	model = BidPurchase
	form_class = BidPurchaseForm
	template_name = 'purchase/purchase_create.html'
	success_url = reverse_lazy('purchase-bid-list')
	permission_required = 'purchase.add_bidpurchase'
	login_url = 'login'

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		StatusBidPurchase.objects.create(bid_id=form.save().id)
		return super(PurchaseCreateView, self).form_valid(form)


class PurchaseUpdateView(PermissionRequiredMixin, UpdateView):
	model = BidPurchase
	form_class = BidPurchaseForm
	success_url = reverse_lazy('purchase-bid-list')
	template_name = 'purchase/purchase_update.html'
	permission_required = 'purchase.add_bidpurchase'
	login_url = 'login'


class PurchaseDeleteView(PermissionRequiredMixin, DeleteView):
	model = BidPurchase
	success_url = reverse_lazy('purchase-bid-list')
	template_name = 'purchase/purchase_delete.html'
	permission_required = 'purchase.delete_bidpurchase'
	login_url = 'login'

	def delete(self, request, *args, **kwargs):
		"""
		Call the delete() method on the fetched object and then redirect to the
		success URL.
		"""
		self.object = self.get_object()
		success_url = self.get_success_url()
		info = f"{self.object.bid_number} {self.object.created_by.first_name}"
		PurchaseDelete.objects.create(info=info)
		self.object.delete()
		return HttpResponseRedirect(success_url)

