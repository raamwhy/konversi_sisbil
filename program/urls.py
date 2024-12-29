# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_tampilan, name='menu_tampilan'),
    path('konversi-desimal/', views.konversi_desimal, name='konversi_desimal'),
    path('konversi-biner/', views.konversi_biner, name='konversi_biner'),
    path('konversi-oktal/', views.konversi_oktal, name='konversi_oktal'),
    path('konversi-heksadesimal/', views.konversi_heksadesimal, name='konversi_heksadesimal'),
    path('result/<int:pk>/', views.result, name='result'),
    path('add/', views.conversion_add, name='conversion_add'),
    path('edit/<int:pk>/', views.conversion_edit, name='conversion_edit'),
    path('delete/<int:pk>/', views.conversion_delete, name='conversion_delete'),
    path('detail/<int:pk>/', views.conversion_detail, name='conversion_detail'),
    path('list/', views.conversion_list, name='conversion_list'),
]
