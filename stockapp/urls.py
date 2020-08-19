from django.urls import path
from .views import ItemList, ItemCreate, ItemDetail, UpDl, plusfunc, mainasfunc
from . import views

urlpatterns = [
    path('', ItemList.as_view(), name='list'),
    path('create/', ItemCreate.as_view(), name='create'),
    path('detail/<int:pk>', ItemDetail.as_view(), name='detail'),
    path('updl/', UpDl.as_view(), name='updl'),
    path('import/', views.PostImport.as_view(), name='import'),
    path('export/', views.PostExport, name='export'),
    path('plus/<int:pk>', plusfunc, name='plus'),
    path('mainas/<int:pk>', mainasfunc, name='mainas'),
]
