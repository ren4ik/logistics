from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import timedelta
from django.db.models import Q, F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.views.generic.base import View
from django.views.generic.edit import FormMixin

from handbook.models import InPathSort, OutPathSort
from logistics.forms import WorkSaleForm, WorkPurchaseForm, PubDateFilterForm, DateFilterForm
from logistics.models import WorkSale, StatusBidSale, OnUploadSale, WorkSaleDelete, OnPathSale, CityClickSale, \
    StatusBidPurchase, WorkPurchase, OnUploadPurchase, WorkPurchaseDelete, OnPathPurchase, CityClickPurchase
from logistics.utils import ObjectDetailMixin
from purchase.models import BidPurchase
from sale.models import BidSale


class HomePageView(PermissionRequiredMixin, TemplateView):
    """домашняя страница"""
    template_name = "home/home.html"
    permission_required = 'handbook.view_cargo'
    login_url = 'login'


class StatusSaleList(PermissionRequiredMixin, FormMixin, ListView):
    """модель статуса заявок - связывает отдел сбыта с отделом логистики"""
    model = StatusBidSale
    template_name = 'logistics/sale/statusbidsale_list.html'
    permission_required = 'logistics.view_statusbidsale'
    login_url = 'login'
    paginate_by = 20
    form_class = DateFilterForm
    ordering = ['-id']

    def get_queryset(self):
        object_list = self.model.objects.filter(status=0)
        query = self.form_class(self.request.GET or None)
        if query.is_valid():
            if query.cleaned_data['min_pub_date'] \
                    and query.cleaned_data['max_pub_date'] \
                    and query.cleaned_data['min_end_date'] \
                    and query.cleaned_data['max_end_date'] \
                    and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['max_pub_date'] \
                    and query.cleaned_data['max_end_date'] \
                    and query.cleaned_data['min_end_date'] \
                    and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                    & Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['min_pub_date'] \
                    and query.cleaned_data['max_end_date'] \
                    and query.cleaned_data['min_end_date'] \
                    and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                    & Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['min_pub_date'] \
                    and query.cleaned_data['max_pub_date'] \
                    and query.cleaned_data['min_end_date'] \
                    and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['min_pub_date'] \
                    and query.cleaned_data['max_pub_date'] \
                    and query.cleaned_data['max_end_date'] \
                    and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['min_pub_date'] \
                    and query.cleaned_data['max_pub_date'] \
                    and query.cleaned_data['max_end_date'] \
                    and query.cleaned_data['min_end_date']:
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                )

            elif query.cleaned_data['min_pub_date'] \
                    and query.cleaned_data['max_end_date'] \
                    and query.cleaned_data['min_end_date']:
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                )

            elif query.cleaned_data['max_pub_date'] \
                    and query.cleaned_data['max_end_date'] \
                    and query.cleaned_data['min_end_date']:
                object_list = object_list.filter(
                    Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                )

            elif query.cleaned_data['min_end_date'] \
                    and query.cleaned_data['max_end_date'] \
                    and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['min_pub_date'] \
                    and query.cleaned_data['max_pub_date'] \
                    and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['min_end_date'] and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['max_end_date'] and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['min_pub_date'] and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['max_pub_date'] and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(status=status)
                )
            elif query.cleaned_data['min_end_date']:
                object_list = object_list.filter(
                    bid__end_date__gte=query.cleaned_data['min_end_date']
                )

            elif query.cleaned_data['max_end_date']:
                object_list = object_list.filter(
                    bid__end_date__lte=query.cleaned_data['max_end_date']
                )
            elif query.cleaned_data['min_pub_date']:
                object_list = object_list.filter(
                    bid__pub_date__gte=query.cleaned_data['min_pub_date']
                )

            elif query.cleaned_data['max_pub_date']:
                object_list = object_list.filter(
                    bid__pub_date__lte=query.cleaned_data['max_pub_date']
                )
            elif query.cleaned_data['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(status=status)
            return object_list

        return object_list


class WorkSaleCreate(PermissionRequiredMixin, CreateView):
    """обработка заявок отделом логистики - отдел сбыта"""
    model = WorkSale
    form_class = WorkSaleForm
    template_name = 'logistics/sale/worksale_create.html'
    success_url = reverse_lazy('work-sale-list')
    permission_required = 'logistics.add_worksale'
    login_url = 'login'

    def form_valid(self, form):
        # содаёт запись в моделе при сохранении статус - +1
        status = StatusBidSale.objects.get(id=form.save().bid.id)
        status.status = 1
        status.save(update_fields=['status'])

        # содаёт запись в моделе при сохранении статус - True
        bid = BidSale.objects.get(id=status.bid_id)
        bid.status = True
        bid.save(update_fields=['status'])

        # содаёт запись в моделе при сохранении статус - False
        OnUploadSale.objects.create(bid_id=form.save().id)
        return super(WorkSaleCreate, self).form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        delta_price = 0
        comment = 'нет комментария'
        num = 'AA 000 UZ'
        bid = get_object_or_404(StatusBidSale, bid=self.kwargs.get('pk'))
        return {
            'created_by': created_by,
            'bid': bid,
            'delta_price': delta_price,
            'comment': comment,
            'num': num

        }


class WorkSaleList(PermissionRequiredMixin, ListView):
    """получение списка заявок, статус обработанные(приняты)"""
    model = WorkSale
    template_name = 'logistics/sale/worksale_list.html'
    permission_required = 'logistics.add_worksale'
    login_url = 'login'
    paginate_by = 20
    ordering = ['-bid_id']


class WorkSaleUpdate(PermissionRequiredMixin, UpdateView):
    """обновление заявки"""
    model = WorkSale
    fields = ['way', 'price', 'delta_price', 'currency', 'num', 'weight','delivery_date', 'comment']
    template_name = 'logistics/sale/worksale_update.html'
    success_url = reverse_lazy('work-sale-list')
    permission_required = 'logistics.add_worksale'
    login_url = 'login'

    def get_initial(self):
        created_by = self.request.user
        bid = get_object_or_404(WorkSale, id=self.kwargs.get('pk'))
        return {
            'created_by': created_by,
            'bid': bid,
        }


class WorkSaleDeleteView(PermissionRequiredMixin, DeleteView):
    """удаление записи"""
    model = WorkSale
    success_url = reverse_lazy('work-sale-list')
    template_name = 'logistics/sale/worksale_delete.html'
    permission_required = 'logistics.delete_worksale'
    login_url = 'login'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        status = StatusBidSale.objects.get(bid_id=self.request.POST.get('id'))
        status.status = 0
        status.save(update_fields=['status'])
        bs = BidSale.objects.get(id=self.request.POST.get('id'))
        bs.status = False
        bs.save(update_fields=['status'])
        info = f"{self.object.bid.bid.bid_number} {self.request.user}"
        WorkSaleDelete.objects.create(info=info)
        self.object.delete()
        return HttpResponseRedirect(success_url)


class UploadSaleUpdate(PermissionRequiredMixin, UpdateView):
    """изменение статуса - на загрузке"""
    model = OnUploadSale
    fields = ['status', 'num']
    template_name = 'logistics/sale/onuploadsale_update.html'
    success_url = reverse_lazy('upload-sale-list')
    permission_required = 'logistics.add_onuploadsale'
    login_url = 'login'

    def form_valid(self, form):
        # содаёт запись в моделе при сохранении статус - +1
        status = StatusBidSale.objects.get(bid_id=form.save().bid.bid.bid_id)
        status.status = 2
        status.save(update_fields=['status'])

        # содаёт запись в моделе при сохранении статус - False
        OnPathSale.objects.create(bid_id=form.save().bid_id)

        # обновляет запись в Work - num
        data = WorkSale.objects.get(bid_id=form.save().bid.bid_id)
        data.num = form.save().num
        data.save(update_fields=['num'])
        return super(UploadSaleUpdate, self).form_valid(form)

    def get_initial(self):
        bid = get_object_or_404(OnUploadSale, id=self.kwargs.get('pk'))
        return {
            'bid': bid,
        }


class UploadSaleList(PermissionRequiredMixin, ListView):
    """список заявок на загрузке"""
    model = OnUploadSale
    template_name = 'logistics/sale/onuploadsale_list.html'
    queryset = OnUploadSale.objects.exclude(status_path=True)
    permission_required = 'logistics.view_onuploadsale'
    login_url = 'login'
    paginate_by = 20


class OnPathSaleUpdate(PermissionRequiredMixin, UpdateView):
    """обновления статуса заявки - в пути"""
    model = OnPathSale
    fields = ['status']
    success_url = reverse_lazy('path-sale-list')
    template_name = 'logistics/sale/onpathsale_update.html'
    permission_required = 'logistics.add_onpathsale'
    login_url = 'login'

    def form_valid(self, form):
        # содаёт запись в моделе при сохранении статус - +1
        status = StatusBidSale.objects.get(bid_id=form.save().bid.bid.bid_id)
        status.status = 3
        status.save(update_fields=['status'])

        # содаёт запись в моделе при сохранении статус - +1
        dx = OnUploadSale.objects.get(bid_id=form.save().bid_id)
        dx.status_path = True
        dx.save(update_fields=['status_path'])

        # содаёт запись в моделе при сохранении статус - False
        CityClickSale.objects.create(bid_id=form.save().bid_id)
        return super(OnPathSaleUpdate, self).form_valid(form)


class OnPathSaleList(PermissionRequiredMixin, ListView):
    """список заявок - в пути"""
    model = OnPathSale
    template_name = 'logistics/sale/onpathsale_list.html'
    queryset = model.objects.exclude(Q(status_path=True) and Q(status=True))
    permission_required = 'logistics.view_onpathsale'
    login_url = 'login'
    paginate_by = 20


class ClickSaleDetail(PermissionRequiredMixin, ObjectDetailMixin, View):
    """вывод городов для обновления по маршруту"""
    model = CityClickSale
    template_name = 'logistics/sale/clicksale_detail.html'
    permission_required = 'logistics.view_cityclicksale'
    login_url = 'login'
    extra_model = OutPathSort


# class ClickSaleUpdate(PermissionRequiredMixin, UpdateView):
#     model = CityClickSale
#     template_name = 'logistics/sale/clicksale_update.html'
#     fields = ['click_count']
#     permission_required = 'logistics.add_cityclicksale'
#     login_url = 'login'
#
#     def get_success_url(self):
#         return reverse('city-click-sale', kwargs={'pk': self.object.pk})
#
#     def form_valid(self, form):
#         # содаёт запись в моделе при сохранении статус - +1
#         eq = CityClickSale.objects.get(id=form.save().id)
#         if eq.click_count == eq.city_count:
#             status = StatusBidSale.objects.get(bid_id=form.save().bid.bid.bid_id)
#             status.status = 4
#             status.save(update_fields=['status'])
#
#             path = OnPathSale.objects.get(bid_id=form.save().bid_id)
#             path.status_path = True
#             path.save(update_fields=['status_path'])
#
#         return super(ClickSaleUpdate, self).form_valid(form)


class ClickSaleList(PermissionRequiredMixin, ListView):
    model = CityClickSale
    template_name = 'logistics/sale/clicksale_list.html'
    permission_required = 'logistics.view_cityclicksale'
    login_url = 'login'
    paginate_by = 20
    queryset = model.objects.all().order_by('bid__bid__status').order_by('bid__bid__bid')
    ordering = ['bid__bid__status', '-bid_id']


green_sale = []
orange_sale = []
red_sale = []
@permission_required('sale.view_bidsale', login_url='/login/')
def all_data_sale(request):

    data = CityClickSale.objects.annotate(diff=F('pub_date') - F('pub_date')).values_list('id', 'diff',
        'bid__delivery_date')

    for foo in data:
        try:
            de = timedelta(days=foo[2]) / foo[1]
        except ZeroDivisionError:
            de = 1
        if de > 0.85:
            green_sale.append(foo)
        elif (0.85 > de) and (de > 0.50):
            orange_sale.append(foo)
        else:
            red_sale.append(foo)
    data_list = f'<span style="color:green">{len(green_sale)} зелёная зона</span>, <span style="color:orange"' \
                f'>{len(orange_sale)} жёлтая' \
                f' зона, </span>' \
                f' <span style="color:red">{len(red_sale)} красная зона </span>'
    green_sale[:] = []
    orange_sale[:] = []
    red_sale[:] = []
    """таблица исходящих заявок"""
    template_name = 'logistics/all_data_sale.html'
    object_list = StatusBidSale.objects.all()

    pub_date_filter = PubDateFilterForm(request.GET or None)
    if pub_date_filter.is_valid():
        if pub_date_filter.cleaned_data['min_pub_date'] \
                and pub_date_filter.cleaned_data['max_pub_date'] \
                and request.GET.get('status'):
            status = int(request.GET.get('status')) - 1
            object_list = object_list.filter(
                Q(bid__pub_date__gte=pub_date_filter.cleaned_data['min_pub_date'])
                & Q(bid__pub_date__lte=pub_date_filter.cleaned_data['max_pub_date'])
            ).filter(status=status)

        elif pub_date_filter.cleaned_data['min_pub_date'] and request.GET.get('status'):
            status = int(request.GET.get('status')) - 1
            object_list = object_list.filter(
                Q(bid__pub_date__gte=pub_date_filter.cleaned_data['min_pub_date'])
                & Q(status=status)
            )

        elif pub_date_filter.cleaned_data['max_pub_date'] and request.GET.get('status'):
            status = int(request.GET.get('status')) - 1
            object_list = object_list.filter(
                Q(bid__pub_date__lte=pub_date_filter.cleaned_data['max_pub_date'])
                & Q(status=status)
            )
        elif pub_date_filter.cleaned_data['min_pub_date']:
            object_list = object_list.filter(
                bid__pub_date__gte=pub_date_filter.cleaned_data['min_pub_date']
            )

        elif pub_date_filter.cleaned_data['max_pub_date']:
            object_list = object_list.filter(
                bid__pub_date__lte=pub_date_filter.cleaned_data['max_pub_date']
            )
        elif pub_date_filter.cleaned_data['status']:
            status = int(request.GET.get('status')) - 1
            object_list = object_list.filter(
                status=status
            )

    paginator = Paginator(object_list, 20)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    mark = False
    args = {
        "data_list": data_list,
        "object_list": object_list,
        "mark": mark,
        "page": page,
        "form_pub": pub_date_filter,
    }
    return render(request, template_name, args)


@permission_required('logistics.view_cityclicksale', login_url='/login/')
def ajax_click_sale(request, pk):
    if request.is_ajax():
        query = CityClickSale.objects.get(id=pk)
        query.click_count = request.GET['id']
        query.save(update_fields=['click_count'])
        work = WorkSale.objects.get(id=query.bid_id)
        status = StatusBidSale.objects.get(id=work.bid_id)
        path = OnPathSale.objects.get(bid_id=query.bid_id)
        f = query.city_count
        d = int(query.click_count)
        s = f - d
        print(pk, f, d, s)
        if s:
            path.status_path = False
            path.save(update_fields=['status_path'])

            status.status = 3
            status.save(update_fields=['status'])
        else:
            path.status_path = True
            path.save(update_fields=['status_path'])

            status.status = 4
            status.save(update_fields=['status'])

        delta_1 = query.pub_date - work.pub_date
        """разница между датой подачи заявки и времени начала движения"""
        try:
            date_p = round(((work.delivery_date / delta_1.days) * 100))
        except ZeroDivisionError:
            date_p = 100
        if delta_1.days == 0:
            class_css = 'green'
        elif date_p >= 85:
            class_css = 'green'
        elif 85 > date_p >= 50:
            class_css = 'orange'
        else:
            class_css = 'red'

        data = {
            'class_css': class_css,
            'click': query.click_count
        }
    else:
        data = {
            'yes': False
        }
    return JsonResponse(data)


@permission_required('logistics.view_cityclicksale', login_url='/login/')
def ajax_sale(request, pk):
    query = CityClickSale.objects.get(id=pk)
    work = WorkSale.objects.get(id=query.bid_id)
    delta_1 = query.pub_date - work.pub_date
    """разница между датой подачи заявки и времени начала движения"""
    try:
        date_p = round(((work.delivery_date / delta_1.days) * 100))
    except ZeroDivisionError:
        date_p = 100
    if delta_1.days == 0:
        class_css = 'green'
    elif date_p >= 85:
        class_css = 'green'
    elif 85 > date_p >= 50:
        class_css = 'orange'
    else:
        class_css = 'red'
    data = {
        'class_css': class_css,
        'id': query.click_count,
        'count': query.city_count,
    }
    return JsonResponse(data)

def ajax_table_sale(request):
    if request.is_ajax():
        num = request.GET.get('dataCount')
    else:
        num = 20
    template_name = 'logistics/ajax-table-sale.html'
    object_list = StatusBidSale.objects.all()[:int(num)]

    args = {
        "object_list": object_list,
    }
    return render(request, template_name, args)

# """Purchase"""


class StatusPurchaseList(PermissionRequiredMixin, FormMixin, ListView):
    """модель статуса заявок - связывает отдел сбыта с отделом логистики"""
    model = StatusBidPurchase
    template_name = 'logistics/purchase/statusbidpurchase_list.html'
    permission_required = 'logistics.view_statusbidpurchase'
    login_url = 'login'
    paginate_by = 20
    form_class = DateFilterForm
    ordering = ['-bid']

    def get_queryset(self):
        object_list = self.model.objects.filter(status=0)
        query = self.form_class(self.request.GET or None)
        if query.is_valid():
            if query.cleaned_data['min_pub_date'] \
                    and query.cleaned_data['max_pub_date'] \
                    and query.cleaned_data['min_end_date'] \
                    and query.cleaned_data['max_end_date'] \
                    and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['max_pub_date'] \
                and query.cleaned_data['max_end_date'] \
                and query.cleaned_data['min_end_date'] \
                and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                    & Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['min_pub_date'] \
                and query.cleaned_data['max_end_date'] \
                and query.cleaned_data['min_end_date'] \
                and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                    & Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['min_pub_date'] \
                and query.cleaned_data['max_pub_date'] \
                and query.cleaned_data['min_end_date'] \
                and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['min_pub_date'] \
                and query.cleaned_data['max_pub_date'] \
                and query.cleaned_data['max_end_date'] \
                and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['min_pub_date'] \
                and query.cleaned_data['max_pub_date'] \
                and query.cleaned_data['max_end_date'] \
                and query.cleaned_data['min_end_date']:
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                )

            elif query.cleaned_data['min_pub_date'] \
                and query.cleaned_data['max_end_date'] \
                and query.cleaned_data['min_end_date']:
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                )

            elif query.cleaned_data['max_pub_date'] \
                and query.cleaned_data['max_end_date'] \
                and query.cleaned_data['min_end_date']:
                object_list = object_list.filter(
                    Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                )

            elif query.cleaned_data['min_end_date'] \
                    and query.cleaned_data['max_end_date'] \
                    and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['min_pub_date'] \
                    and query.cleaned_data['max_pub_date'] \
                    and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['min_end_date'] and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__end_date__gte=query.cleaned_data['min_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['max_end_date'] and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__end_date__lte=query.cleaned_data['max_end_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['min_pub_date'] and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__gte=query.cleaned_data['min_pub_date'])
                    & Q(status=status)
                )

            elif query.cleaned_data['max_pub_date'] and self.request.GET['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(
                    Q(bid__pub_date__lte=query.cleaned_data['max_pub_date'])
                    & Q(status=status)
                )
            elif query.cleaned_data['min_end_date']:
                object_list = object_list.filter(
                    bid__end_date__gte=query.cleaned_data['min_end_date']
                )

            elif query.cleaned_data['max_end_date']:
                object_list = object_list.filter(
                    bid__end_date__lte=query.cleaned_data['max_end_date']
                )
            elif query.cleaned_data['min_pub_date']:
                object_list = object_list.filter(
                    bid__pub_date__gte=query.cleaned_data['min_pub_date']
                )

            elif query.cleaned_data['max_pub_date']:
                object_list = object_list.filter(
                    bid__pub_date__lte=query.cleaned_data['max_pub_date']
                )
            elif query.cleaned_data['status']:
                status = int(self.request.GET['status']) - 1
                object_list = object_list.filter(status=status)
            return object_list

        return object_list


class WorkPurchaseCreate(PermissionRequiredMixin, CreateView):
    """обработка заявок отделом логистики - отдел сбыта"""
    model = WorkPurchase
    form_class = WorkPurchaseForm
    template_name = 'logistics/purchase/workpurchase_create.html'
    success_url = reverse_lazy('work-purchase-list')
    permission_required = 'logistics.add_workpurchase'
    login_url = 'login'

    def form_valid(self, form):
        # содаёт запись в моделе при сохранении статус - +1
        status = StatusBidPurchase.objects.get(id=form.save().bid.id)
        status.status = 1
        status.save(update_fields=['status'])

        # содаёт запись в моделе при сохранении статус - True
        bid = BidPurchase.objects.get(id=status.bid_id)
        bid.status = True
        bid.save(update_fields=['status'])

        # содаёт запись в моделе при сохранении статус - False
        OnUploadPurchase.objects.create(bid_id=form.save().id)
        return super(WorkPurchaseCreate, self).form_valid(form)

    def get_initial(self):
        created_by = self.request.user
        delta_price = 0
        comment = 'нет комментария'
        num = 'AA 000 UZ'
        bid = get_object_or_404(StatusBidPurchase, bid=self.kwargs.get('pk'))
        return {
            'created_by': created_by,
            'bid': bid,
            'delta_price': delta_price,
            'comment': comment,
            'num': num
        }


class WorkPurchaseList(PermissionRequiredMixin, ListView):
    """получение списка заявок, статус обработанные(приняты)"""
    model = WorkPurchase
    template_name = 'logistics/purchase/workpurchase_list.html'
    permission_required = 'logistics.view_workpurchase'
    login_url = 'login'
    paginate_by = 20
    ordering = ['-bid_id']


class WorkPurchaseUpdate(PermissionRequiredMixin, UpdateView):
    """обновление заявки"""
    model = WorkPurchase
    fields = ['way', 'price', 'delta_price', 'currency', 'num', 'weight', 'delivery_date', 'comment']
    template_name = 'logistics/purchase/workpurchase_update.html'
    success_url = reverse_lazy('work-purchase-list')
    permission_required = 'logistics.add_workpurchase'
    login_url = 'login'

    def get_initial(self):
        created_by = self.request.user
        bid = get_object_or_404(WorkPurchase, id=self.kwargs.get('pk'))
        return {
            'created_by': created_by,
            'bid': bid,
        }


class WorkPurchaseDeleteView(PermissionRequiredMixin, DeleteView):
    """удаление записи"""
    model = WorkPurchase
    success_url = reverse_lazy('work-purchase-list')
    template_name = 'logistics/purchase/workpurchase_delete.html'
    permission_required = 'logistics.delete_workpurchase'
    login_url = 'login'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        status = StatusBidPurchase.objects.get(bid_id=self.request.POST.get('id'))
        status.status = 0
        status.save(update_fields=['status'])
        bs = BidPurchase.objects.get(id=self.request.POST.get('id'))
        bs.status = False
        bs.save(update_fields=['status'])
        info = f"{self.object.bid.bid.bid_number} {self.request.user}"
        WorkPurchaseDelete.objects.create(info=info)
        self.object.delete()
        return HttpResponseRedirect(success_url)


class UploadPurchaseUpdate(PermissionRequiredMixin, UpdateView):
    """изменение статуса - на загрузке"""
    model = OnUploadPurchase
    fields = ['status', 'num']
    template_name = 'logistics/purchase/onuploadpurchase_update.html'
    success_url = reverse_lazy('upload-purchase-list')
    permission_required = 'logistics.add_onuploadpurchase'
    login_url = 'login'

    def form_valid(self, form):
        # содаёт запись в моделе при сохранении статус - +1
        status = StatusBidPurchase.objects.get(bid_id=form.save().bid.bid.bid_id)
        status.status = 2
        status.save(update_fields=['status'])

        # содаёт запись в моделе при сохранении статус - False
        OnPathPurchase.objects.create(bid_id=form.save().bid_id)

        # обновляет запись в Work - num
        num = WorkPurchase.objects.get(bid_id=form.save().bid.bid_id)
        num.num = form.save().num
        num.save(update_fields=['num'])
        return super(UploadPurchaseUpdate, self).form_valid(form)

    def get_initial(self):
        bid = get_object_or_404(OnUploadPurchase, id=self.kwargs.get('pk'))
        return {
            'bid': bid,
        }


class UploadPurchaseList(PermissionRequiredMixin, ListView):
    """список заявок на загрузке"""
    model = OnUploadPurchase
    template_name = 'logistics/purchase/onuploadpurchase_list.html'
    queryset = OnUploadPurchase.objects.exclude(status_path=True).order_by('bid_id')
    permission_required = 'logistics.view_onuploadpurchase'
    login_url = 'login'
    paginate_by = 20


class OnPathPurchaseUpdate(PermissionRequiredMixin, UpdateView):
    """обновления статуса заявки - в пути"""
    model = OnPathPurchase
    fields = ['status']
    success_url = reverse_lazy('path-purchase-list')
    template_name = 'logistics/purchase/onpathpurchase_update.html'
    permission_required = 'logistics.add_onpathpurchase'
    login_url = 'login'

    def form_valid(self, form):
        # содаёт запись в моделе при сохранении статус - +1
        status = StatusBidPurchase.objects.get(bid_id=form.save().bid.bid.bid_id)
        status.status = 3
        status.save(update_fields=['status'])

        # содаёт запись в моделе при сохранении статус - +1
        dx = OnUploadPurchase.objects.get(bid_id=form.save().bid_id)
        dx.status_path = True
        dx.save(update_fields=['status_path'])

        # содаёт запись в моделе при сохранении статус - False
        CityClickPurchase.objects.create(bid_id=form.save().bid_id)
        return super(OnPathPurchaseUpdate, self).form_valid(form)


class OnPathPurchaseList(PermissionRequiredMixin, ListView):
    """список заявок - в пути"""
    model = OnPathPurchase
    template_name = 'logistics/purchase/onpathpurchase_list.html'
    queryset = model.objects.exclude(Q(status_path=True) and Q(status=True))
    permission_required = 'logistics.view_onpathpurchase'
    login_url = 'login'
    paginate_by = 20


class ClickPurchaseDetail(PermissionRequiredMixin, ObjectDetailMixin, View):
    """вывод городов для обновления по маршруту"""
    model = CityClickPurchase
    template_name = 'logistics/purchase/clickpurchase_detail.html'
    permission_required = 'logistics.view_cityclickpurchase'
    login_url = 'login'
    extra_model = InPathSort


# class ClickPurchaseUpdate(PermissionRequiredMixin, UpdateView):
#     model = CityClickPurchase
#     template_name = 'logistics/purchase/clickpurchase_update.html'
#     fields = ['click_count']
#     permission_required = 'logistics.add_cityclickpurchase'
#     login_url = 'login'
#
#     def get_success_url(self):
#         return reverse('city-click-purchase', kwargs={'pk': self.object.pk})
#
#     def form_valid(self, form):
#         # содаёт запись в моделе при сохранении статус - +1
#         eq = CityClickPurchase.objects.get(id=form.save().id)
#         if eq.click_count == eq.city_count:
#             status = StatusBidPurchase.objects.get(bid_id=form.save().bid.bid.bid_id)
#             status.status = 4
#             status.save(update_fields=['status'])
#
#             path = OnPathPurchase.objects.get(bid_id=form.save().bid_id)
#             path.status_path = True
#             path.save(update_fields=['status_path'])
#
#         return super(ClickPurchaseUpdate, self).form_valid(form)


class ClickPurchaseList(PermissionRequiredMixin, ListView):
    model = CityClickPurchase
    template_name = 'logistics/purchase/clickpurchase_list.html'
    permission_required = 'logistics.view_cityclickpurchase'
    login_url = 'login'
    paginate_by = 20
    queryset = model.objects.all().order_by('bid__bid__status').order_by('bid__bid__bid')
    ordering = ['bid__bid__status', '-bid_id']

green_purchase = []
orange_purchase = []
red_purchase = []

@permission_required('purchase.view_bidpurchase', login_url='/login/')
def all_data_purchase(request):
    from datetime import timedelta
    data = CityClickPurchase.objects.annotate(diff=F('pub_date') - F('update_date')).values_list('id', 'diff',
        'bid__delivery_date')

    for foo in data:
        try:
            de = timedelta(days=foo[2]) / foo[1]
        except ZeroDivisionError:
            de = 1
        if de > 0.85:
            green_purchase.append(foo)
        elif (0.85 > de) and (de > 0.50):
            orange_purchase.append(foo)
        else:
            red_purchase.append(foo)
    data_list = f'<span style="color:green">{len(green_purchase)} зелёная зона</span>, <span style="color:orange">{len(orange_purchase)} жёлтая' \
                f' зона, </span>' \
                f' <span style="color:red">{len(red_purchase)} красная зона </span>'

    green_purchase[:] = []
    orange_purchase[:] = []
    red_purchase[:] = []

    """таблица входящих заявок"""
    template_name = 'logistics/all_data_purchase.html'
    object_list = StatusBidPurchase.objects.all()

    pub_date_filter = PubDateFilterForm(request.GET or None)
    # print(request.GET.get('min_pub_date'))

    if pub_date_filter.is_valid():
        if pub_date_filter.cleaned_data['min_pub_date'] \
                and pub_date_filter.cleaned_data['max_pub_date'] \
                and request.GET.get('status'):
            status = int(request.GET.get('status')) - 1
            object_list = object_list.filter(
                Q(bid__pub_date__gte=pub_date_filter.cleaned_data['min_pub_date'])
                & Q(bid__pub_date__lte=pub_date_filter.cleaned_data['max_pub_date'])
            ).filter(status=status)

        elif pub_date_filter.cleaned_data['min_pub_date'] and request.GET.get('status'):
            status = int(request.GET.get('status')) - 1
            object_list = object_list.filter(
                Q(bid__pub_date__gte=pub_date_filter.cleaned_data['min_pub_date'])
                & Q(status=status)
            )

        elif pub_date_filter.cleaned_data['max_pub_date'] and request.GET.get('status'):
            status = int(request.GET.get('status')) - 1
            object_list = object_list.filter(
                Q(bid__pub_date__lte=pub_date_filter.cleaned_data['max_pub_date'])
                & Q(status=status)
            )
        elif pub_date_filter.cleaned_data['min_pub_date']:
            object_list = object_list.filter(
                bid__pub_date__gte=pub_date_filter.cleaned_data['min_pub_date']
            )

        elif pub_date_filter.cleaned_data['max_pub_date']:
            object_list = object_list.filter(
                bid__pub_date__lte=pub_date_filter.cleaned_data['max_pub_date']
            )
        elif pub_date_filter.cleaned_data['status']:
            status = int(request.GET.get('status')) - 1
            object_list = object_list.filter(
                status=status
            )

    paginator = Paginator(object_list, 20)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    mark = True
    args = {
        "data_list": data_list,
        "object_list": object_list,
        "mark": mark,
        "page": page,
        "form_pub": pub_date_filter,
    }
    return render(request, template_name, args)


@permission_required('logistics.view_cityclickpurchase', login_url='/login/')
def ajax_click_purchase(request, pk):
    if request.is_ajax():
        query = CityClickPurchase.objects.get(id=pk)
        query.click_count = request.GET['id']
        query.save(update_fields=['click_count'])
        work = WorkPurchase.objects.get(id=query.bid_id)
        status = StatusBidPurchase.objects.get(id=work.bid_id)
        path = OnPathPurchase.objects.get(bid_id=query.bid_id)

        f = query.city_count
        d = int(query.click_count)
        s = f - d

        print(f, d, s)
        if s:
            path.status_path = False
            path.save(update_fields=['status_path'])

            status.status = 3
            status.save(update_fields=['status'])
        else:
            path.status_path = True
            path.save(update_fields=['status_path'])

            status.status = 4
            status.save(update_fields=['status'])

        delta_1 = query.pub_date - work.pub_date
        """разница между датой подачи заявки и времени начала движения"""
        try:
            date_p = round(((work.delivery_date / delta_1.days) * 100))
        except ZeroDivisionError:
            date_p = 100
        if delta_1.days == 0:
            class_css = 'green'
        elif date_p >= 85:
            class_css = 'green'
        elif 85 > date_p >= 50:
            class_css = 'orange'
        else:
            class_css = 'red'

        data = {
            'class_css': class_css,
            'click': query.click_count
        }
        return JsonResponse(data)


@permission_required('logistics.view_cityclickpurchase', login_url='/login/')
def ajax_purchase(request, pk):
    query = CityClickPurchase.objects.get(id=pk)
    work = WorkPurchase.objects.get(id=query.bid_id)
    delta_1 = query.pub_date - work.pub_date
    """разница между датой подачи заявки и времени начала движения"""

    try:
        date_p = round(((work.delivery_date / delta_1.days) * 100))
    except ZeroDivisionError:
        date_p = 100
    if delta_1.days == 0:
        class_css = 'green'
    elif date_p >= 85:
        class_css = 'green'
    elif 85 > date_p >= 50:
        class_css = 'orange'
    else:
        class_css = 'red'
    data = {
        'class_css': class_css,
        'id': query.click_count,
        'count': query.city_count,
    }
    return JsonResponse(data)


def ajax_table_purchase(request):
    if request.is_ajax():
        num = request.GET.get('dataCount')
    else:
        num = 20
    template_name = 'logistics/ajax-table-purchase.html'
    object_list = StatusBidPurchase.objects.all()[:int(num)]

    args = {
        "object_list": object_list,
    }
    return render(request, template_name, args)

# def test(request):
#     # data1 = CityClickPurchase.objects.filter(bid__delivery_date__lte=2)
#     # data2 = WorkPurchase.objects.all().values('pub_date')
#     # #data = list(data1) + list(data2)
#     from django.db.models import Count, Max
#     # data = CityClickPurchase.objects.values('id', 'pub_date', 'bid__delivery_date', 'bid__pub_date')
#
#     from datetime import timedelta
#     data = CityClickPurchase.objects.annotate(diff=F('pub_date') - F('bid__pub_date')).values_list('id', 'diff', 'bid__delivery_date')
#
#     for foo in data:
#         if  (foo[1] / timedelta(days=foo[2])) > 0.85:
#             green_list.append(foo)
#         elif 0.85 > (foo[1] / timedelta(days=foo[2])) > 0.50:
#             orange_list.append(foo)
#         else:
#             red_list.append(foo)
#     print(f'{len(green_list)} зелёная зона, {len(orange_list)} жёлтая зона, {len(red_list)} красная зона')
#
#
#     # data_json = serializers.serialize('json', data)
#     return HttpResponse(data)