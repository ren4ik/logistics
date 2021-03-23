from django.db import models
from django.contrib.auth.models import User

from handbook.models import *


class BidSale(models.Model):
	"""заявка отдела сбыта"""
	created_by = models.ForeignKey(
		User,
		verbose_name="Заявитель",
		on_delete=models.PROTECT,
		null=True
	)
	bid_number = models.PositiveIntegerField(
		verbose_name="Номер заявки",
		default=1234567
	)
	cargo = models.ManyToManyField(
		Cargo,
		verbose_name="Грузы",
		related_name="cargoes"
	)
	end_date = models.DateField(
		verbose_name="Крайний срок",
		blank=False,
		null=True
	)
	client = models.ForeignKey(
		Client,
		verbose_name="клиент",
		on_delete=models.PROTECT,
		null=True
	)
	comment = models.TextField(
		verbose_name="Примечание",
		blank=True,
		default=""
	)
	pub_date = models.DateField(
		verbose_name="Дата создания",
		auto_now_add=True,
		blank=True,
		null=True,
		editable=False
	)
	update_date = models.DateField(
		verbose_name="Дата изменения",
		auto_now=True,
		blank=True,
		null=True,
		editable=False
	)
	file = models.FileField(
		verbose_name="Файл",
		upload_to="uploads/%Y/%m/%d/",
		blank=True,
		default="",
		max_length=100,
	)
	status = models.BooleanField(verbose_name="Статус", default=False, blank=True)

	class Meta:
		verbose_name = "Заявка отдела сбыта"
		verbose_name_plural = "Заявки отдела сбыта"
		ordering = ['-id']

	def __str__(self):
		return f"{self.bid_number}"

	def get_absolute_url(self):
		return reverse('sale-bid', kwargs={'pk': self.pk})


class SaleDelete(models.Model):
	"""кто и когда удалил заявку"""
	info = models.CharField(verbose_name="info", max_length=200)
	date = models.DateTimeField(verbose_name="дата удаления", auto_now_add=True, blank=True)

	class Meta:
		verbose_name = "Удалил"
		verbose_name_plural = "Удалили"
		ordering = ['-date']

	def __str__(self):
		return f'{self.info}-{self.date}'

