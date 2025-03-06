from django.db import models
from django.contrib.auth.models import User


class Fasilitas(models.Model):
    nama = models.CharField(max_length=255)
    tipe = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.nama

    class Meta:
        db_table = 'fasilitas'


class Kegiatan(models.Model):
    nama = models.CharField(max_length=255)

    def __str__(self):
        return self.nama

    class Meta:
        db_table = 'kegiatan'

class Masjid(models.Model):
    name = models.CharField(max_length=255)
    deskripsi = models.TextField()
    tipe = models.TextField()
    address = models.TextField()
    tahun = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    photo = models.ImageField(upload_to='foto/', null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    fasilitas = models.ManyToManyField("Fasilitas", through="MasjidFasilitas", blank=True)
    kegiatan = models.ManyToManyField("Kegiatan", through="MasjidKegiatan", blank=True)
    class Meta:
      db_table = 'masjid'
    def __str__(self):
        return self.name



class MasjidFasilitas(models.Model):
    masjid = models.ForeignKey(Masjid, on_delete=models.CASCADE)
    fasilitas = models.ForeignKey(Fasilitas, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('masjid', 'fasilitas')
        db_table = 'masjid_fasilitas'

class MasjidKegiatan(models.Model):
    masjid = models.ForeignKey(Masjid, on_delete=models.CASCADE)
    kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('masjid', 'kegiatan')
        db_table = 'masjid_kegiatan'


