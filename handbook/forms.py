from django import forms
from .models import *


class OutPathForm(forms.ModelForm):
	city = forms.ModelMultipleChoiceField(
		queryset=City.objects.all(),
		widget=forms.CheckboxSelectMultiple,
		required=False,
		label="Города"
	)

	class Meta:
		model = OutPath
		exclude = ('date_input', 'date_update', 'code_path')


class InPathForm(forms.ModelForm):
	city = forms.ModelMultipleChoiceField(
		queryset=City.objects.all(),
		widget=forms.CheckboxSelectMultiple,
		required=False,
		label="Города"
	)

	class Meta:
		model = InPath
		exclude = ('date_input', 'date_update', 'code_path')


# class OutSortForm(forms.Form):
# 	path_code = forms.IntegerField(label="Код маршрута")
# 	city = forms.IntegerField(label="")
# 	class Meta:
# 		model = OutPathSort
# 		fields = ['path_code', 'city', 'sort']


class InSortForm(forms.ModelForm):

	class Meta:
		model = InPathSort
		fields = ['path_code', 'city', 'sort']
