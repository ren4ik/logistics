from django.shortcuts import render


class ObjectDetailMixin:
	model = None
	template_name = None
	url = None
	extra_model = None
	permission_required = None
	login_url = None

	def get(self, request, pk):
		obj = self.model.objects.get(pk=pk)
		auto = self.extra_model.objects.filter(path_code=obj.bid.way_id)

		args = {
			"object": obj,
			"auto": auto
		}
		return render(request, self.template_name, args)