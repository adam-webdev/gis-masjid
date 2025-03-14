from django import forms
from .models import Masjid, Fasilitas, Kegiatan

class MasjidForm(forms.ModelForm):
    fasilitas = forms.ModelMultipleChoiceField(
    queryset=Fasilitas.objects.all(),
    widget=forms.CheckboxSelectMultiple,
    required=False
    )
    kegiatan = forms.ModelMultipleChoiceField(
        queryset=Kegiatan.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Masjid
        fields = ['name', 'address','tahun','tipe','fasilitas','kegiatan','deskripsi','latitude','longitude','photo','contact']

class FasilitasForm(forms.ModelForm):
    class Meta:
        model = Fasilitas
        fields = ['nama','tipe']

class KegiatanForm(forms.ModelForm):
    class Meta:
        model = Kegiatan
        fields = ['nama']

class MasjidImportForm(forms.ModelForm):
    file = forms.FileField()