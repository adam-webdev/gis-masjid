# Generated by Django 5.1.6 on 2025-03-03 05:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mosque', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fasilitas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'fasilitas',
            },
        ),
        migrations.CreateModel(
            name='Kegiatan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'kegiatan',
            },
        ),
        migrations.CreateModel(
            name='Masjid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('deskripsi', models.TextField()),
                ('tipe', models.TextField()),
                ('address', models.TextField()),
                ('tahun', models.IntegerField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='foto/')),
                ('contact', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MasjidFasilitas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fasilitas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mosque.fasilitas')),
                ('masjid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mosque.masjid')),
            ],
            options={
                'db_table': 'masjid_fasilitas',
                'unique_together': {('masjid', 'fasilitas')},
            },
        ),
        migrations.CreateModel(
            name='MasjidKegiatan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kegiatan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mosque.kegiatan')),
                ('masjid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mosque.masjid')),
            ],
            options={
                'db_table': 'masjid_kegiatan',
                'unique_together': {('masjid', 'kegiatan')},
            },
        ),
    ]
