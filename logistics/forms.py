from django import forms
from django.contrib.auth.models import User

from handbook.models import *
from logistics.models import WorkSale, StatusBidSale, StatusBidPurchase, WorkPurchase


class WorkSaleForm(forms.ModelForm):
	created_by = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
	bid = forms.ModelChoiceField(queryset=StatusBidSale.objects.all(), widget=forms.HiddenInput)
	trade_term = forms.ModelMultipleChoiceField(queryset=TradeTerm.objects.all(), label="Торговые термины")
	delivery_date = forms.IntegerField(label="Дни доставки")
	shipping_date = forms.DateField(label="Дата погрузки")
	price = forms.IntegerField(label="Цена")
	currency = forms.ModelChoiceField(queryset=Currency.objects.all(), label="Валюта")
	way = forms.ModelChoiceField(queryset=OutPath.objects.all(), label="Исходяший маршрут")
	path = forms.ModelChoiceField(queryset=Path.objects.all(), label="Вид")
	num = forms.CharField(widget=forms.HiddenInput, required=False)
	comment = forms.CharField(widget=forms.HiddenInput, required=False)
	provider = forms.ModelChoiceField(queryset=LogisticsProvider.objects.all(), label="Поставщик услуг", )
	delta_price = forms.IntegerField(widget=forms.HiddenInput, )
	weight = forms.CharField(label="Вес")

	weight.widget.attrs.update({'class': 'uk-input'})
	provider.widget.attrs.update({'class': 'uk-select'})
	path.widget.attrs.update({'class': 'uk-select'})
	trade_term.widget.attrs.update({'class': 'uk-select'})
	way.widget.attrs.update({'class': 'uk-select'})
	delivery_date.widget.attrs.update({'class': 'uk-input'})
	price.widget.attrs.update({'class': 'uk-input'})
	currency.widget.attrs.update({'class': 'uk-select'})
	shipping_date.widget.attrs.update({'class': 'uk-input'})

	class Meta:
		model = WorkSale
		exclude = (
			'pub_date',
			'update_date'
		)


class WorkPurchaseForm(forms.ModelForm):
	created_by = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
	bid = forms.ModelChoiceField(queryset=StatusBidPurchase.objects.all(), widget=forms.HiddenInput)
	trade_term = forms.ModelMultipleChoiceField(queryset=TradeTerm.objects.all(), label="Торговые термины")
	delivery_date = forms.IntegerField(label="Дни доставки")
	shipping_date = forms.DateField(label="Дата погрузки")
	price = forms.IntegerField(label="Цена")
	currency = forms.ModelChoiceField(queryset=Currency.objects.all(), label="Валюта")
	way = forms.ModelChoiceField(queryset=InPath.objects.all(), label="Входяший маршрут")
	path = forms.ModelChoiceField(queryset=Path.objects.all(), label="Вид")
	num = forms.CharField(widget=forms.HiddenInput, required=False)
	comment = forms.CharField(widget=forms.HiddenInput, required=False)
	provider = forms.ModelChoiceField(queryset=LogisticsProvider.objects.all(), label="Поставщик услуг",)
	delta_price = forms.IntegerField(widget=forms.HiddenInput, )
	weight = forms.CharField(label="Вес")

	weight.widget.attrs.update({'class': 'uk-input'})
	provider.widget.attrs.update({'class': 'uk-select'})
	path.widget.attrs.update({'class': 'uk-select'})
	trade_term.widget.attrs.update({'class': 'uk-select'})
	way.widget.attrs.update({'class': 'uk-select'})
	delivery_date.widget.attrs.update({'class': 'uk-input'})
	price.widget.attrs.update({'class': 'uk-input'})
	currency.widget.attrs.update({'class': 'uk-select'})
	shipping_date.widget.attrs.update({'class': 'uk-input'})

	class Meta:
		model = WorkPurchase
		exclude = (
			'pub_date',
			'update_date'
		)


class PubDateFilterForm(forms.Form):
	min_pub_date = forms.DateField(label='Дата подачи заявки \"c\"', required=False)
	max_pub_date = forms.DateField(label='до', required=False)
	status = forms.ModelChoiceField(queryset=Status.objects.all(), label='статус', required=False)

	min_pub_date.widget.attrs.update({'class': 'uk-input'})
	max_pub_date.widget.attrs.update({'class': 'uk-input'})
	status.widget.attrs.update({'class': 'uk-select'})


class DateFilterForm(forms.Form):
	min_pub_date = forms.DateField(label='Дата подачи заявки \"c\"', required=False)
	max_pub_date = forms.DateField(label='до', required=False)
	min_end_date = forms.DateField(label='Крайний срок \"c\"', required=False)
	max_end_date = forms.DateField(label='до', required=False)
	status = forms.ModelChoiceField(queryset=Status.objects.all(), label='статус', required=False)

	min_pub_date.widget.attrs.update({'class': 'uk-input'})
	max_pub_date.widget.attrs.update({'class': 'uk-input'})
	min_end_date.widget.attrs.update({'class': 'uk-input'})
	max_end_date.widget.attrs.update({'class': 'uk-input'})
	status.widget.attrs.update({'class': 'uk-select'})



