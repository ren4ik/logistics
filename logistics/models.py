from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from handbook.models import OutPath, Transport, InPath, TradeTerm, Currency, Path, LogisticsProvider
from purchase.models import BidPurchase
from sale.models import BidSale


class StatusBidSale(models.Model):
	"""статус заявок от отдела сбыта"""
	bid = models.OneToOneField(
		BidSale,
		verbose_name="номер заявки",
		on_delete=models.CASCADE,
		related_name="bidsale",
		null=True
	)
	status = models.PositiveSmallIntegerField(verbose_name="статус заявки", default=0, blank=True)
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

	class Meta:
		verbose_name = "Статус заявки отдела сбыта"
		verbose_name_plural = "Статусы заявок отдела сбыта"
		ordering = ['-bid_id', '-status']

	def __str__(self):
		return f'{self.bid}'

	def get_absolute_url(self):
		return reverse('status-bid-sale', kwargs={'pk': self.pk})


class StatusBidPurchase(models.Model):
	"""статус заявок от отдела закупа"""
	bid = models.OneToOneField(
		BidPurchase,
		verbose_name="номер заявки",
		on_delete=models.CASCADE,
		related_name="bidpurchase",
		null=True
	)
	status = models.PositiveSmallIntegerField(verbose_name="статус заявки", default=0, blank=True)
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

	class Meta:
		verbose_name = "Статус заявки отдела закупа"
		verbose_name_plural = "Статусы заявок отдела закупа"
		ordering = ['-bid_id', '-status']

	def __str__(self):
		return f'{self.bid}'

	def get_absolute_url(self):
		return reverse('status-bid-purchase', kwargs={'pk': self.pk})


class WorkSale(models.Model):
	"""рабочая модель записями по заявке от сбыта(транспорт, маршрут и т.д.)"""
	created_by = models.ForeignKey(User, verbose_name="Сотрудник", on_delete=models.CASCADE, default=1, blank=True)
	bid = models.OneToOneField(
		StatusBidSale,
		verbose_name="номер заявки",
		related_name="statussale",
		on_delete=models.CASCADE,
	)
	way = models.ForeignKey(
		OutPath,
		verbose_name="код маршрута",
		on_delete=models.SET_NULL,
		blank=False,
		null=True,
	)
	price = models.PositiveIntegerField(verbose_name="цена услуги", blank=True, null=False)
	delta_price = models.PositiveIntegerField(verbose_name="новая цена", blank=True, default=0)
	currency = models.ForeignKey(Currency, verbose_name="Валюта", on_delete=models.CASCADE, default=1)
	"""добавляется при сохранении Upload"""
	num = models.CharField(
		verbose_name="номер машины",
		max_length=50,
		default="FF 0000 UZ"
	)
	weight = models.CharField(verbose_name="вес", max_length=100, default=0)
	path = models.ForeignKey(Path, verbose_name="Вид", on_delete=models.CASCADE, default=1)
	trade_term = models.ManyToManyField(TradeTerm, verbose_name="Торговые термины", related_name="term2")
	comment = models.TextField(
		verbose_name="Примечание",
		blank=True,
		default=""
	)
	provider = models.ForeignKey(LogisticsProvider, verbose_name="Поставщик услуг", on_delete=models.CASCADE)
	delivery_date = models.PositiveSmallIntegerField(verbose_name="Дни доставки", default=3)
	shipping_date = models.DateField(
		verbose_name="дата погрузки",
		editable=True,
		null=False,
		blank=False
	)
	pub_date = models.DateField(
		verbose_name="Дата создания",
		auto_now_add=True,
		editable=False,
		null=False,
		blank=True
	)
	update_date = models.DateField(
		verbose_name="Дата обновления",
		auto_now=True,
		editable=False,
		null=False,
		blank=True
	)

	class Meta:
		verbose_name = "обработка заявки отдела сбыта"
		verbose_name_plural = "обработка заявок отдела сбыта"
		ordering = ['-bid_id']

	def __str__(self):
		return f"{self.bid_id}"

	def get_absolute_url(self):
		return reverse('work-sale', kwargs={'pk': self.pk})


class WorkPurchase(models.Model):
	"""рабочая модель записями по заявке от закупа(транспорт, маршрут и т.д.)"""
	created_by = models.ForeignKey(User, verbose_name="Сотрудник", on_delete=models.CASCADE, default=1, blank=True)
	bid = models.OneToOneField(
		StatusBidPurchase,
		verbose_name="номер заявки",
		on_delete=models.CASCADE,
		related_name="statuspurchase",
		null=True,
		default="1"
	)
	way = models.ForeignKey(
		InPath,
		verbose_name="код маршрута",
		on_delete=models.SET_NULL,
		blank=False,
		null=True,
	)
	price = models.PositiveIntegerField(verbose_name="цена услуги", blank=True, default=0)
	currency = models.ForeignKey(Currency, verbose_name="Валюта", on_delete=models.CASCADE, default=1)
	delta_price = models.PositiveIntegerField(verbose_name="новая цена", blank=True, default=0, null=True)
	provider = models.ForeignKey(LogisticsProvider, verbose_name="Поставщик услуг", on_delete=models.CASCADE, default=1)

	trade_term = models.ManyToManyField(TradeTerm, verbose_name="Торговые термины", related_name="term")
	"""добавляется при сохранении Upload"""
	num = models.CharField(
		verbose_name="номер машины",
		max_length=50,
		blank=True,
		default="FF 0000 UZ"
	)
	weight = models.CharField(verbose_name="вес", max_length=100, default=0)
	comment = models.TextField(
		verbose_name="Примечание",
		blank=True,
		default=""
	)

	path = models.ForeignKey(Path, verbose_name="Вид", on_delete=models.CASCADE, default=1)
	delivery_date = models.PositiveSmallIntegerField(verbose_name="Дни доставки", default=3)
	shipping_date = models.DateField(
		verbose_name="дата погрузки",
		editable=True,
		null=True,
		blank=False
	)
	pub_date = models.DateField(
		verbose_name="Дата создания",
		auto_now_add=True,
		editable=False,
		null=True,
		blank=True
	)
	update_date = models.DateField(
		verbose_name="Дата обновления",
		auto_now=True,
		editable=False,
		null=True,
		blank=True
	)

	class Meta:
		verbose_name = "обработка заявки отдела закупа"
		verbose_name_plural = "обработка заявок отдела закупа"
		ordering = ['bid__bid_id']

	def __str__(self):
		return f"{self.bid_id}"

	def get_absolute_url(self):
		return reverse('work-purchase', kwargs={'pk': self.pk})


class WorkSaleDelete(models.Model):
	"""кто и когда удалил заявку"""
	info = models.CharField(verbose_name="info", max_length=200)
	date = models.DateTimeField(verbose_name="дата удаления", auto_now_add=True, blank=True)

	class Meta:
		verbose_name = "Удалил"
		verbose_name_plural = "Удалили"
		ordering = ['-date']

	def __str__(self):
		return f'{self.info}-{self.date}'


class WorkPurchaseDelete(models.Model):
	"""кто и когда удалил заявку"""
	info = models.CharField(verbose_name="info", max_length=200)
	date = models.DateTimeField(verbose_name="дата удаления", auto_now_add=True, blank=True)

	class Meta:
		verbose_name = "Удалил"
		verbose_name_plural = "Удалили"
		ordering = ['-date']

	def __str__(self):
		return f'{self.info}-{self.date}'


class OnUploadSale(models.Model):
	"""статус завки отдела сбыта на загрузке"""
	bid = models.OneToOneField(
		WorkSale,
		verbose_name="на загрузке",
		related_name="onupsale",
		on_delete=models.CASCADE,
		null=True
	)
	num = models.CharField(
		verbose_name="номер машины",
		max_length=50,
		default="FF 0000 UZ"
	)
	status = models.BooleanField(default=False, blank=True)
	pub_date = models.DateField(
		verbose_name="Дата создания",
		auto_now_add=True,
		editable=False,
		null=True,
		blank=True
	)
	update_date = models.DateField(
		verbose_name="Дата обновления",
		auto_now=True,
		editable=False,
		null=True,
		blank=True
	)
	status_path = models.BooleanField(default=False, blank=True)

	class Meta:
		verbose_name = "на загрузке - отдела сбыта"
		verbose_name_plural = "на загрузке - отдела сбыта"
		ordering = ['-bid__bid__id', '-status']

	def __str__(self):
		return f"{self.bid}"

	def get_absolute_url(self):
		return reverse('on-upload-sale', kwargs={'pk': self.pk})


class OnUploadPurchase(models.Model):
	"""статус завки отдела закупа на загрузке"""
	bid = models.OneToOneField(
		WorkPurchase,
		verbose_name="на загрузке",
		related_name="onuppurchase",
		on_delete=models.CASCADE,
		null=True
	)
	num = models.CharField(
		verbose_name="номер машины",
		max_length=50,
		default="FF 0000 UZ"
	)
	status = models.BooleanField(default=False, blank=True)
	pub_date = models.DateField(
		verbose_name="Дата создания",
		auto_now_add=True,
		editable=False,
		null=True,
		blank=True
	)
	update_date = models.DateField(
		verbose_name="Дата обновления",
		auto_now=True,
		editable=False,
		null=True,
		blank=True
	)
	status_path = models.BooleanField(default=False, blank=True)

	class Meta:
		verbose_name = "на загрузке - отдела закупа"
		verbose_name_plural = "на загрузке - отдела закупа"
		ordering = ['-bid__bid__id', '-status']

	def __str__(self):
		return f"{self.bid}"

	def get_absolute_url(self):
		return reverse('on-upload-purchase', kwargs={'pk': self.pk})


class OnPathSale(models.Model):
	"""статус завки отдела сбыта в пути"""
	bid = models.OneToOneField(
		WorkSale,
		verbose_name="в пути",
		related_name="onpathsale",
		on_delete=models.CASCADE,
		null=True
	)
	status = models.BooleanField(default=False, blank=True)
	pub_date = models.DateField(
		verbose_name="Дата создания",
		auto_now_add=True,
		editable=False,
		null=True,
		blank=True
	)
	update_date = models.DateField(
		verbose_name="Дата обновления",
		auto_now=True,
		editable=False,
		null=True,
		blank=True
	)
	status_path = models.BooleanField(default=False, blank=True)

	class Meta:
		verbose_name = "в пути - отдел сбыта"
		verbose_name_plural = "в пути - отдел сбыта"
		ordering = ['-bid__bid__id', '-status']

	def __str__(self):
		return f"{self.bid}"

	def get_absolute_url(self):
		return reverse('on-path-sale', kwargs={'pk': self.pk})


class OnPathPurchase(models.Model):
	"""статус завки отдела закупа в пути"""
	bid = models.OneToOneField(
		WorkPurchase,
		verbose_name="в пути",
		related_name="onpathpurchase",
		on_delete=models.CASCADE,
		null=True
	)
	status = models.BooleanField(default=False, blank=True)
	pub_date = models.DateField(
		verbose_name="Дата создания",
		auto_now_add=True,
		editable=False,
		null=True,
		blank=True
	)
	update_date = models.DateField(
		verbose_name="Дата обновления",
		auto_now=True,
		editable=False,
		null=True,
		blank=True
	)
	status_path = models.BooleanField(default=False, blank=True)

	class Meta:
		verbose_name = "в пути - отдел закупа"
		verbose_name_plural = "в пути - отдел закупа"
		ordering = ['-bid__bid__id', '-status']

	def __str__(self):
		return f"{self.bid}"

	def get_absolute_url(self):
		return reverse('on-path-purchase', kwargs={'pk': self.pk})


class CityClickSale(models.Model):
	"""изменение статуса нахождения груза по городам - сбыт"""
	bid = models.OneToOneField(
		WorkSale,
		verbose_name="город на пути",
		related_name="cityonpathsale",
		on_delete=models.CASCADE,
		null=True
	)
	city_count = models.PositiveSmallIntegerField(verbose_name="кол-во городов", default=0, blank=True)
	click_count = models.PositiveSmallIntegerField(verbose_name="кол-во кликов", default=0, blank=True)
	pub_date = models.DateField(
		verbose_name="Дата создания",
		auto_now_add=True,
		editable=False,
		null=True,
		blank=True
	)
	update_date = models.DateField(
		verbose_name="Дата обновления",
		auto_now=True,
		editable=False,
		null=True,
		blank=True
	)

	class Meta:
		verbose_name = "заявки отдела сбыта"
		ordering = ['-bid_id']

	def __str__(self):
		return f"{self.bid}"

	def get_absolute_url(self):
		return reverse('city-click-sale', kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):
		self.city_count = self.city_sum()
		super(CityClickSale, self).save(*args, **kwargs)

	def city_sum(self):
		return OutPath.objects.get(id=self.bid.way_id).city.count()


class CityClickPurchase(models.Model):
	"""изменение статуса нахождения груза по городам - закуп"""
	bid = models.OneToOneField(
		WorkPurchase,
		verbose_name="город на пути",
		related_name="cityonpathpurchase",
		on_delete=models.CASCADE,
		null=True
	)
	city_count = models.PositiveSmallIntegerField(verbose_name="кол-во городов", default=0, blank=True)
	click_count = models.PositiveSmallIntegerField(verbose_name="кол-во кликов", default=0, blank=True)
	pub_date = models.DateField(
		verbose_name="Дата создания",
		auto_now_add=True,
		editable=False,
		null=True,
		blank=True
	)
	update_date = models.DateField(
		verbose_name="Дата обновления",
		auto_now=True,
		editable=False,
		null=True,
		blank=True
	)

	class Meta:
		verbose_name = "заявки отдела закупа"
		ordering = ['-bid_id']

	def __str__(self):
		return f"{self.bid_id}"

	def get_absolute_url(self):
		return reverse('city-click-purchase', kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):
		self.city_count = self.city_sum()
		super(CityClickPurchase, self).save(*args, **kwargs)

	def city_sum(self):
		return InPath.objects.get(id=self.bid.way_id).city.count()
