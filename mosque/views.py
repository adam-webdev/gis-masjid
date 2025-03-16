
from django.urls import path, reverse_lazy
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render, redirect
from .models import Masjid, Fasilitas, MasjidFasilitas, Kegiatan, MasjidKegiatan
from .forms import MasjidForm,FasilitasForm,KegiatanForm,MasjidImportForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
import json
from django.core.serializers import serialize
from django.http import JsonResponse
import pandas as pd
from django.contrib import messages
from django.contrib.auth import authenticate, login


def login_view(request):
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("dashboard")  # Ganti dengan URL dashboard
            else:
                messages.error(request, "Username atau password salah!")

        return render(request, "admin/login.html")
# Dashboard View
class DashboardView(LoginRequiredMixin,ListView):
    model = Masjid
    template_name = 'masjidview/dashboard.html'
    login_url = '/login/'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        # context['masjid_count'] = Masjid.objects.count()
        context['meunasah_count'] = Masjid.objects.filter(tipe="meunasah").count()
        context['masjid_count'] = Masjid.objects.exclude(tipe="meunasah").count()
        context['fasilitas_count'] = Fasilitas.objects.count()  # Total fasilitas
        context['kegiatan_count'] = Kegiatan.objects.count()  # Total kegiatan
        return context
# class HomeView(ListView):
#     model = Masjid
#     template_name = 'masjidview/home.html'
#     print("masjid",Masjid)
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         masjid_data = list(Masjid.objects.values())  # Konversi ke list of dict
#         context['masjid'] = json.dumps(masjid_data)  # Konversi ke JSON
#         return context



class HomeView(ListView):
    model = Masjid
    template_name = 'masjidview/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Ambil semua masjid dengan fasilitas & kegiatan
        masjid_list = Masjid.objects.prefetch_related('fasilitas', 'kegiatan')

        # Konversi data ke format JSON
        masjid_data = []
        for masjid in masjid_list:
            # Buat dictionary untuk masjid
            masjid_dict = {
                "id": masjid.id,
                "nama": masjid.name,
                "deskripsi": masjid.deskripsi if masjid.deskripsi else "",
                "tahun": masjid.tahun if masjid.tahun else "",
                "contact": masjid.contact if masjid.contact else "",
                "address": masjid.address if masjid.address else "",
                "lat": masjid.latitude if masjid.latitude else 0.0,
                "lon": masjid.longitude if masjid.longitude else 0.0,
                "foto": masjid.photo.url if masjid.photo else None,
                "fasilitas": [
                    {"nama": fasilitas.nama, "tipe": fasilitas.tipe}
                    for fasilitas in masjid.fasilitas.all()
                ] if masjid.fasilitas.exists() else [],  # ⬅ Tambahkan ini
                "kegiatan": [kegiatan.nama for kegiatan in masjid.kegiatan.all()] if masjid.kegiatan.exists() else [],  # ⬅ Tambahkan ini
            }

            # Pengelompokan fasilitas berdasarkan tipe
            fasilitas_grouped = {}
            if masjid.fasilitas.exists():  # ⬅ Tambahkan pengecekan
                for fasilitas in masjid.fasilitas.all():
                    tipe = fasilitas.tipe
                    if tipe not in fasilitas_grouped:
                        fasilitas_grouped[tipe] = []
                    fasilitas_grouped[tipe].append(fasilitas.nama)

            # Tambahkan hasil pengelompokan ke masjid_dict
            masjid_dict["fasilitas_grouped"] = fasilitas_grouped if fasilitas_grouped else {}  # ⬅ Jika kosong, tetap dict kosong

            # Masukkan ke dalam list masjid_data
            masjid_data.append(masjid_dict)

        # Kirim ke template dalam format JSON
        context['masjid_html'] = masjid_data
        context['masjid'] = json.dumps(masjid_data)  # Jika ingin digunakan dalam JavaScript
        return context

# HomeDetail
class HomeDetailView(DetailView):
    model = Masjid
    template_name = 'masjidview/masjid_detail.html'
    context_object_name = 'masjid_detail'  # Supaya di template bisa pakai `masjid_detail` langsung

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        masjid = self.object  # Objek masjid yang sesuai pk sudah otomatis tersedia

        masjid_dict = {
            "id": masjid.id,
            "nama": masjid.name,
            "deskripsi": masjid.deskripsi,
            "tahun": masjid.tahun,
            "contact": masjid.contact,
            "address": masjid.address,
            "lat": masjid.latitude,
            "lon": masjid.longitude,
            "foto": masjid.photo.url if masjid.photo else None,
            "fasilitas": [
                {"nama": fasilitas.nama, "tipe": fasilitas.tipe}
                for fasilitas in masjid.fasilitas.all()
            ],
            "kegiatan": [kegiatan.nama for kegiatan in masjid.kegiatan.all()],
        }

        # Pengelompokan fasilitas berdasarkan tipe
        fasilitas_grouped = {}
        for fasilitas in masjid.fasilitas.all():
            tipe = fasilitas.tipe
            if tipe not in fasilitas_grouped:
                fasilitas_grouped[tipe] = []
            fasilitas_grouped[tipe].append(fasilitas.nama)

        masjid_dict["fasilitas_grouped"] = fasilitas_grouped

        context['masjid_detail'] = masjid_dict
        return context

# Masjid Views
class MasjidListView(ListView):
    model = Masjid
    paginate_by  = 10
    template_name = 'masjidview/masjid.html'
    context_object_name = 'masjid'


class MasjidCreateView(CreateView):
    model = Masjid
    form_class = MasjidForm
    template_name = 'masjidview/masjidform.html'
    success_url = reverse_lazy('masjid')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Ambil semua fasilitas dan kelompokkan berdasarkan tipe
        fasilitas_list = Fasilitas.objects.all().order_by('tipe')
        fasilitas_grouped = {}

        for fasilitas in fasilitas_list:
            if fasilitas.tipe not in fasilitas_grouped:
                fasilitas_grouped[fasilitas.tipe] = []
            fasilitas_grouped[fasilitas.tipe].append(fasilitas)
        context['fasilitas_grouped'] = fasilitas_grouped
        return context

class MasjidUpdateView(UpdateView):
    model = Masjid
    form_class = MasjidForm
    template_name = 'masjidview/masjidform.html'
    success_url = reverse_lazy('masjid')

    def get_object(self, queryset=None):
        return get_object_or_404(Masjid, pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        masjid = self.get_object()

        # Ambil semua fasilitas dan kelompokkan berdasarkan tipe
        fasilitas_list = Fasilitas.objects.all().order_by('tipe')
        fasilitas_grouped = {}

        for fasilitas in fasilitas_list:
            if fasilitas.tipe not in fasilitas_grouped:
                fasilitas_grouped[fasilitas.tipe] = []
            fasilitas_grouped[fasilitas.tipe].append({
                'id': fasilitas.id,
                'nama': fasilitas.nama,
                'checked': fasilitas in masjid.fasilitas.all()  # Cek apakah fasilitas sudah dipilih
            })

        context['fasilitas_grouped'] = fasilitas_grouped
        return context

class MasjidDeleteView(DeleteView):
    model = Masjid
    template_name = 'masjidview/masjid_confirm_delete.html'
    success_url = reverse_lazy('masjid')
# Fasilitas Views
class FasilitasListView(ListView):
    model = Fasilitas
    template_name = 'fasilitas/fasilitas.html'
    paginate_by  = 3
    context_object_name = 'fasilitas'

class FasilitasCreateView(CreateView):
    model = Fasilitas
    form_class = FasilitasForm
    template_name = 'fasilitas/fasilitasform.html'
    success_url = reverse_lazy('fasilitas_list')

class FasilitasUpdateView(UpdateView):
    form_class = FasilitasForm
    model = Fasilitas
    template_name = 'fasilitas/fasilitasform.html'
    success_url = reverse_lazy('fasilitas_list')

class FasilitasDeleteView(DeleteView):
    model = Fasilitas
    template_name = 'fasilitas/fasilitas_confirm_delete.html'
    success_url = reverse_lazy('fasilitas_list')

# Kegiatan Views
class KegiatanListView(ListView):
    model = Kegiatan
    paginate_by  = 10
    template_name = 'kegiatan/kegiatan.html'
    context_object_name = 'kegiatan'

class KegiatanCreateView(CreateView):
    form_class = KegiatanForm
    model = Kegiatan
    template_name = 'kegiatan/kegiatanform.html'
    success_url = reverse_lazy('kegiatan_list')

class KegiatanUpdateView(UpdateView):
    model = Kegiatan
    form_class = KegiatanForm
    template_name = 'kegiatan/kegiatanform.html'
    success_url = reverse_lazy('kegiatan_list')

class KegiatanDeleteView(DeleteView):
    model = Kegiatan
    template_name = 'kegiatan/kegiatan_confirm_delete.html'
    success_url = reverse_lazy('kegiatan_list')




def import_masjid_excel(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']

        try:
            df = pd.read_excel(file, engine='openpyxl',skiprows=2)
            print(df.head())
            # Looping data dan simpan ke database
            for _, row in df.iterrows():
                Masjid.objects.update_or_create(
                    id=row['ID'],  # Pastikan kolom di Excel ada 'ID'
                    defaults={
                        "name": row['Nama'],
                        "tipe": row['Tipe'],
                        "deskripsi": row['Deskripsi'],
                        "tahun": row['Tahun'],
                        "contact": row['Kontak'],
                        "address": row['Alamat'],
                        "latitude": row['Latitude'],
                        "longitude": row['Longitude'],
                    }
                )

            messages.success(request, "Data berhasil diimport!")
            return redirect('import-masjid')  # Ganti dengan URL yang sesuai

        except Exception as e:
            messages.error(request, f"Terjadi kesalahan: {e}")

    return render(request, 'masjidview/import_excel.html')
