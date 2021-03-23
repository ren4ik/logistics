from django import forms
from handbook.models import *
from sale.models import BidSale


class BidSaleForm(forms.ModelForm):
	bid_number = forms.IntegerField(label="Номер заявки")
	cargo = forms.ModelMultipleChoiceField(queryset=Cargo.objects.all(), label="Груз")
	end_date = forms.CharField(label="Крайний срок")
	client = forms.ModelChoiceField(queryset=Client.objects.all(), label="Клиент")
	comment = forms.CharField(widget=forms.Textarea, max_length=200, label="Примечание")

	cargo.widget.attrs.update({'class': 'uk-select'})
	bid_number.widget.attrs.update({'class': 'uk-input'})
	end_date.widget.attrs.update({'class': 'uk-input'})
	client.widget.attrs.update({'class': 'uk-input'})
	comment.widget.attrs.update({'class': 'uk-textarea'})

	class Meta:
		model = BidSale
		exclude = (
			'created_by',
			'status',
			'pub_date',
			'update_date'
		)
