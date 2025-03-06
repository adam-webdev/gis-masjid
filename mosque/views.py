from django.urls import path, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from .models import Masjid, Fasilitas, MasjidFasilitas, Kegiatan, MasjidKegiatan
from .forms import MasjidForm,FasilitasForm,KegiatanForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
# Dashboard View
class DashboardView(ListView):
    model = Masjid
    template_name = 'masjidview/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['masjid_count'] = Masjid.objects.count()
        context['fasilitas_count'] = Fasilitas.objects.count()  # Total fasilitas
        context['kegiatan_count'] = Kegiatan.objects.count()  # Total kegiatan
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

class MasjidUpdateView(UpdateView):
    model = Masjid
    form_class = MasjidForm
    template_name = 'masjidview/masjidform.html'
    success_url = reverse_lazy('masjid')

    def get_object(self, queryset=None):
        return get_object_or_404(Masjid, pk=self.kwargs.get("pk"))

class MasjidDeleteView(DeleteView):
    model = Masjid
    template_name = 'masjidview/masjid_confirm_delete.html'
    success_url = reverse_lazy('masjid')
# Fasilitas Views
class FasilitasListView(ListView):
    model = Fasilitas
    template_name = 'fasilitas/fasilitas.html'
    paginate_by  = 10
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



