import csv
import io
import urllib
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, FormView
from .models import ItemModel
from django.urls import reverse_lazy
from .forms import CSVUploadForm
from .models import ItemModel
# Create your views here.


class ItemList(ListView):
    template_name = 'list.html'
    model = ItemModel


class ItemCreate(CreateView):
    template_name = 'create.html'
    model = ItemModel
    fields = ('name', 'productname', 'company', 'stocknum')
    success_url = reverse_lazy('list')


class ItemDetail(DetailView):
    template_name = 'detail.html'
    model = ItemModel


class UpDl(ListView):
    template_name = 'updl.html'
    model = ItemModel


class PostImport(FormView):
    """
    役職テーブルの登録(csvアップロード)
    """
    template_name = 'import.html'
    success_url = reverse_lazy('updl')
    form_class = CSVUploadForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_name'] = 'csvdownload'
        return ctx

    def form_valid(self, form):
        """postされたCSVファイルを読み込み、役職テーブルに登録します"""
        csvfile = io.TextIOWrapper(form.cleaned_data['file'])
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            """
            役職テーブルを役職コード(primary key)で検索します
            """
            item, created = ItemModel.objects.get_or_create(pk=row[0])
            item.name = row[1]
            item.productname = row[2]
            item.company = row[3]
            item.stocknum = row[4]
            item.save()
        return super().form_valid(form)


def PostExport(request):
    response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
    filename = urllib.parse.quote((u'CSVファイル.csv').encode("utf8"))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)
    writer = csv.writer(response)
    writer.writerow(['No', '一般名称', '商品名', 'メーカー名', '在庫数'])
    for item in ItemModel.objects.all():
        writer.writerow([item.pk, item.name, item.productname, item.company, item.stocknum])
    return response


def plusfunc(request, pk):
    post = ItemModel.objects.get(pk=pk)
    post.stocknum += 1
    post.save()
    return redirect('detail', pk=pk)


def mainasfunc(request, pk):
    post = ItemModel.objects.get(pk=pk)
    if post.stocknum > 0:
        post.stocknum -= 1
        post.save()
        return redirect('detail', pk=pk)
    else:
        return redirect('detail', pk=pk)
