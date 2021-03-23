from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from handbook.models import Transport


class ObjectDetailMixin:
	model = None
	template_name = None
	url = None

	def get(self, request):

		object_list = self.model.objects.all()
		paginator = Paginator(object_list, 20)
		page = request.GET.get('page')
		try:
			object_list = paginator.page(page)
		except PageNotAnInteger:
			object_list = paginator.page(1)
		except EmptyPage:
			object_list = paginator.page(paginator.num_pages)
		return render(request, self.template_name, {
			'object_list': object_list,
			'page': page,
		})

	def post(self, request):
		object_list = self.model.objects.all()
		if request.method == 'POST':
			if request.POST.get('update'):
				idx = request.POST.get('id')
				obj = self.model.objects.get(id=idx)
				obj.name = request.POST.get('name')
				obj.save()
				return HttpResponseRedirect(self.url)
			elif request.POST.get('delete'):
				idx = request.POST.get('id')
				obj = self.model.objects.get(id=idx)
				obj.delete()
				return HttpResponseRedirect(self.url)
			else:
				name = request.POST.get('name')
				q = self.model.objects.filter(name__iexact=name).exists()
				if q:
					info = True
					args = {
						'object_list': object_list,
						'info': info,
						'name': name
					}
					return render(request, self.template_name, args)
				else:
					self.model.objects.create(name=name)
					return HttpResponseRedirect(self.url)


class ObjectDetailMixin2:
	model = None
	template_name = None
	url = None
	form_name = None

	def get(self, request):
		object_list = self.model.objects.all()
		form = self.form_name()
		paginator = Paginator(object_list, 20)
		page = request.GET.get('page')
		try:
			object_list = paginator.page(page)
		except PageNotAnInteger:
			object_list = paginator.page(1)
		except EmptyPage:
			object_list = paginator.page(paginator.num_pages)
		return render(request, self.template_name, {
			'form': form,
			'object_list': object_list,
			'page': page,
		})

	def post(self, request):
		if request.POST.get('create'):
			form = self.form_name(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(self.url)
		elif request.POST.get('update'):
			idx = request.POST.get('id')
			obj = self.model.objects.get(id=idx)
			description = request.POST.get('description')
			lists = list(request.POST.getlist('city'))
			obj.description = description
			ins = self.model(id=idx, description=description, code_path=obj.code_path)
			ins.save()
			ins.city.set(lists)
			return HttpResponseRedirect(self.url)
		else:
			idx = request.POST.get('id')
			obj = self.model.objects.get(id=idx)
			obj.delete()
			return HttpResponseRedirect(self.url)


class ObjectDetailMixin3:
	model = None
	extra_model = None
	template_name = None
	url = None

	# form_name = OutSortForm

	def get(self, request, pk):
		request.session['path_id'] = pk
		obj = self.extra_model.objects.get(pk=pk)
		city_list = self.model.objects.filter(path_code=pk)
		name = obj.__class__.__name__.lower()
		city = city_list.exists()
		transport = Transport.objects.all()
		city_max = obj.city.all().count()
		city_max += 1
		max_city = [i for i in range(0, city_max)]

		return render(request, self.template_name, {
			'obj': obj,
			'city': city,
			'city_list': city_list,
			'transport': transport,
			'max_city': max_city,
			'name': name
		})

	def post(self, request, pk):

		city = request.POST.get('city')
		sort = request.POST.get('sort')
		transport = request.POST.get('transport')

		if self.model.objects.filter(Q(path_code_id=pk) & Q(sort=sort)).exists():
			return HttpResponseRedirect(self.url)
		else:
			if self.model.objects.filter(Q(path_code_id=pk) & Q(city_id=city) & Q(sort=sort)).exists():
				obj = self.extra_model.objects.get(pk=pk)
				city_list = self.model.objects.filter(path_code=pk)
				city = city_list.exists()
				return render(request, self.template_name, {
					'obj': obj,
					'city': city,
					'city_list': city_list,
				})
			elif self.model.objects.filter(Q(path_code_id=pk) & Q(city_id=city)).exists():
				data = self.model.objects.get(Q(path_code_id=pk) & Q(city_id=city))
				data.sort = sort
				data.save(update_fields=["sort"])
				return HttpResponseRedirect(self.url)
			else:
				q = self.model(path_code_id=pk, city_id=city, sort=sort, transport_id=transport)
				q.save()
				return HttpResponseRedirect(self.url)
