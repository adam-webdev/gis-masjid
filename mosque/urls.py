from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LogoutView

from .views import (
    DashboardView,
    MasjidListView,
    MasjidCreateView,
    MasjidUpdateView,
    MasjidDeleteView,
    FasilitasListView,
    FasilitasCreateView,
    FasilitasUpdateView,
    FasilitasDeleteView,
    KegiatanListView,
    KegiatanCreateView,
    KegiatanUpdateView,
    KegiatanDeleteView,
)

urlpatterns = [
     path('admin/', admin.site.urls),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='/admin/login/'), name='logout'),
    # Masjid
    path('masjid/', MasjidListView.as_view(), name='masjid'),
    path('masjid/add/', MasjidCreateView.as_view(), name='masjid_create'),
    path('masjid/edit/<int:pk>/', MasjidUpdateView.as_view(), name='masjid_edit'),
    path('masjid/delete/<int:pk>/', MasjidDeleteView.as_view(), name='masjid_delete'),

    # Fasilitas
    path('fasilitas/', FasilitasListView.as_view(), name='fasilitas_list'),
    path('fasilitas/add/', FasilitasCreateView.as_view(), name='fasilitas_create'),
    path('fasilitas/edit/<int:pk>/', FasilitasUpdateView.as_view(), name='fasilitas_edit'),
    path('fasilitas/delete/<int:pk>/', FasilitasDeleteView.as_view(), name='fasilitas_delete'),

    # Kegiatan
    path('kegiatan/', KegiatanListView.as_view(), name='kegiatan_list'),
    path('kegiatan/add/', KegiatanCreateView.as_view(), name='kegiatan_create'),
    path('kegiatan/edit/<int:pk>/', KegiatanUpdateView.as_view(), name='kegiatan_edit'),
    path('kegiatan/delete/<int:pk>/', KegiatanDeleteView.as_view(), name='kegiatan_delete'),
]
