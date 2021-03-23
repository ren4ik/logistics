import random

from django.db import models
from django.urls import reverse


class City(models.Model):
	"""города"""
	name = models.CharField(
		verbose_name="город",
		max_length=100,
		unique=True,
		default="city",
	)

	class Meta:
		verbose_name = "город"
		verbose_name_plural = "города"
		ordering = ['name']

	def get_absolute_url(self):
		reverse('city', kwargs={'pk': self.id})

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.upper()
		super(City, self).save(*args, **kwargs)


class OutPath(models.Model):
	"""номера маршрутов исходящего"""
	description = models.CharField(
		verbose_name="Описание маршрута",
		blank=False,
		max_length=100,
		default="UZ-?"
	)
	code_path = models.PositiveIntegerField(
		verbose_name="код маршрута",
		unique=True,
		null=True,
		blank=True
	)
	city = models.ManyToManyField(
		City,
		verbose_name="города",
		related_name="out_path"
	)
	date_input = models.DateField(
		verbose_name="Дата создания",
		auto_now_add=True,
		editable=False,
		null=True,
		blank=True
	)
	date_update = models.DateField(
		verbose_name="Дата обновления",
		auto_now=True,
		editable=False,
		null=True,
		blank=True
	)

	class Meta:
		verbose_name = "маршрут исходящий"
		verbose_name_plural = "маршруты исходящие"

	def __str__(self):
		return f"{self.code_path}/{self.description}"

	def save(self, *args, **kwargs):
		self.code_path = self.get_code()
		super(OutPath, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('out-path-sort', kwargs={'pk': self.pk})

	def get_code(self):
		k = OutPath.objects.filter(id=self.id).exists()
		if k:
			return self.code_path
		else:
			r = random.randint(1, 10000)
			self.code_path = 100000 + r
			return self.code_path


class InPath(models.Model):
	"""Маршрут входящий"""
	description = models.CharField(
		verbose_name="Описание маршрута",
		blank=False,
		max_length=100,
		default="?-UZ"
	)
	city = models.ManyToManyField(
		City,
		verbose_name="города",
		related_name="in_path"
	)
	code_path = models.PositiveIntegerField(
		"код маршрута",
		unique=True,
		blank=True,
		editable=False,
	)
	date_input = models.DateField(
		verbose_name="Дата создания",
		auto_now_add=True,
		editable=False,
		null=True,
		blank=True
	)
	date_update = models.DateField(
		verbose_name="Дата обновления",
		auto_now=True,
		editable=False,
		null=True,
		blank=True
	)

	class Meta:
		verbose_name = "маршрут входящий"
		verbose_name_plural = "маршруты входящие"

	def __str__(self):
		return f"{self.code_path}/{self.description}"

	def save(self, *args, **kwargs):
		self.code_path = self.get_code()
		super(InPath, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('in-path-sort', kwargs={'pk': self.pk})

	def get_code(self):
		k = InPath.objects.filter(id=self.id).exists()
		if k:
			return self.code_path
		else:
			r = random.randint(1, 10000)
			self.code_path = 100000 + r
			return self.code_path

	def get_transport(self):
		return InPathSort.objects.filter(path_code=self.code_path)


class Client(models.Model):
	"""клиент которому поставляется груз"""
	name = models.CharField(
		verbose_name="клиет",
		max_length=200,
		blank=False,
		null=False,
		default="client",
		unique=True
	)

	class Meta:
		verbose_name = "клиет"
		verbose_name_plural = "клиеты"
		ordering = ['name']

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.upper()
		super(Client, self).save(*args, **kwargs)


class Provider(models.Model):
	"""поставщик груза по заявкам от закупщиков"""
	name = models.CharField(
		verbose_name="поставщик",
		max_length=200,
		blank=False,
		null=False,
		default="provider",
		unique=True
	)

	class Meta:
		verbose_name = "поставщик"
		verbose_name_plural = "поставщики"
		ordering = ['name']

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.upper()
		super(Provider, self).save(*args, **kwargs)


class Status(models.Model):
	"""статусы"""
	name = models.CharField(
		"Статус",
		max_length=20,
		unique=True,
		blank=False,
		default="status",
		null=False
	)

	class Meta:
		verbose_name = "Статус"
		verbose_name_plural = "Статусы"
		ordering = ['id']

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.upper()
		super(Status, self).save(*args, **kwargs)


class Cargo(models.Model):
	"""название грузов"""
	name = models.CharField(
		"материал",
		max_length=200,
		blank=False,
		null=False,
		default="cargo",
		unique=True
	)

	class Meta:
		verbose_name = "материал"
		verbose_name_plural = "материалы"
		ordering = ['name']

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.upper()
		super(Cargo, self).save(*args, **kwargs)


class TradeTerm(models.Model):
	"""торговые термины"""
	name = models.CharField(
		verbose_name="торговы термин",
		max_length=10,
		null=False,
		blank=False,
		default="example"
	)

	class Meta:
		verbose_name = "торговый термин"
		verbose_name_plural = "торговые термины"
		ordering = ['name']

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.upper()
		super(TradeTerm, self).save(*args, **kwargs)


class Transport(models.Model):
	name = models.CharField(
		"Транспорт",
		max_length=20,
		unique=True,
		blank=False,
		null=False,
		default="example"
	)

	class Meta:
		verbose_name = "Транспорт"
		verbose_name_plural = "Транспорт"
		ordering = ['name']

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.upper()
		super(Transport, self).save(*args, **kwargs)


class OutPathSort(models.Model):
	"""сортировка городов в маршруте"""
	path_code = models.ForeignKey(
		OutPath,
		verbose_name="код исходящего маршрута",
		on_delete=models.CASCADE,
		related_name="out_path"
	)
	city = models.ForeignKey(City, verbose_name="города", on_delete=models.CASCADE)
	sort = models.PositiveSmallIntegerField(verbose_name="ключ сортировки")
	transport = models.ForeignKey(
		Transport,
		verbose_name="транспорт",
		on_delete=models.SET_NULL,
		blank=False,
		null=True,
	)

	class Meta:
		ordering = ['path_code', 'sort']
		verbose_name = "Сортировка по исходящему маршруту"
		verbose_name_plural = "Сортировка по исходящем маршрутам"

	def __str__(self):
		return f"{self.path_code}/{self.city}/{self.sort}"

	def city_out(self):
		count = OutPath.objects.get(pk=self.path_code)
		city_list = count.city.filter(city_name=count.pk)
		return city_list


class InPathSort(models.Model):
	path_code = models.ForeignKey(
		InPath,
		verbose_name="код входящего маршрута",
		on_delete=models.CASCADE,
		related_name="in_path"
	)
	city = models.ForeignKey(
		City,
		verbose_name="города",
		on_delete=models.CASCADE
	)
	sort = models.PositiveSmallIntegerField(verbose_name="ключ сортировки")
	transport = models.ForeignKey(
		Transport,
		verbose_name="транспорт",
		on_delete=models.SET_NULL,
		blank=False,
		null=True,
	)

	class Meta:
		ordering = ['path_code', 'sort']
		verbose_name = "Сортировка по входящему маршруту"
		verbose_name_plural = "Сортировка по входящим маршрутам"

	def __str__(self):
		return f"{self.path_code}/{self.city}/{self.sort}"

	def city_in(self):
		count = InPath.objects.get(pk=self.path_code)
		city_list = count.city.filter(city_name=count.pk)
		return city_list


class Currency(models.Model):
	name = models.CharField(verbose_name="Валюта", max_length=10, default="сум")

	class Meta:
		verbose_name = "Валюта"
		verbose_name_plural = "Валюты"
		ordering = ['name']

	def __str__(self):
		return self.name


class Path(models.Model):
	"""вид маршрута loc, imp, exp"""
	name = models.CharField(verbose_name="Вид", max_length=50)

	class Meta:
		verbose_name = "Вид"
		verbose_name_plural = "Виды"
		ordering = ['name']

	def __str__(self):
		return self.name


class LogisticsProvider(models.Model):
	"""поставщик услуг для логиста"""
	name = models.CharField(verbose_name="Поставщик услуг", max_length=50)

	class Meta:
		verbose_name = "Поставщик"
		verbose_name_plural = "Поставщики"
		ordering = ['name']

	def __str__(self):
		return self.name


