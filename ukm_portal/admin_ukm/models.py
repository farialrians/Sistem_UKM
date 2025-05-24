from django.db import models
from django.contrib.auth.models import User
# Remove PostgreSQL-specific import
# from django.contrib.postgres.fields import ArrayField
from datetime import time, datetime
from tinymce.models import HTMLField
import json

class UKM(models.Model):
    nama = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='ukm_logos/', null=True, blank=True)
    deskripsi_singkat = HTMLField()
    visi = HTMLField()
    misi = HTMLField()
    JENIS_KEGIATAN_CHOICES = (
        ('seni', 'Seni'),
        ('olahraga', 'Olahraga'),
        ('akademik', 'Akademik'),
        ('sosial', 'Sosial'),
        ('teknologi', 'Teknologi'),
        ('lainnya', 'Lainnya'),
    )
    jenis_kegiatan = models.CharField(max_length=50, choices=JENIS_KEGIATAN_CHOICES)
    HARI_CHOICES = (
        ('senin', 'Senin'),
        ('selasa', 'Selasa'),
        ('rabu', 'Rabu'),
        ('kamis', 'Kamis'),
        ('jumat', 'Jumat'),
        ('sabtu', 'Sabtu'),
        ('minggu', 'Minggu'),
    )
    hari_mulai = models.CharField(max_length=20, choices=HARI_CHOICES)
    hari_selesai = models.CharField(max_length=20, choices=HARI_CHOICES)
    waktu_mulai = models.TimeField(default=time(8, 0))
    waktu_selesai = models.TimeField(default=time(17, 0))
    ketua_ukm = models.CharField(max_length=100)
    pengurus_pendaftaran = models.CharField(max_length=100)
    persyaratan_umum = HTMLField()
    BERKAS_CHOICES = (
        ('ktm', 'KTM'),
        ('pas_foto', 'Pas Foto'),
        ('cv', 'CV'),
        ('surat_minat', 'Surat Minat'),
        ('lainnya', 'Lainnya'),
    )
    # Replace ArrayField with TextField to store JSON
    berkas_dibutuhkan_json = models.TextField(default='[]')
    
    ALUR_PENDAFTARAN_CHOICES = (
        ('online', 'Pendaftaran Online'),
        ('seleksi', 'Seleksi Berkas'),
        ('wawancara', 'Wawancara'),
        ('pengumuman', 'Pengumuman'),
    )
    # Replace ArrayField with TextField to store JSON
    alur_pendaftaran_json = models.TextField(default='[]')
    
    periode_pendaftaran_mulai = models.DateField(null=True, blank=True)
    periode_pendaftaran_selesai = models.DateField(null=True, blank=True)
    admin_ukm = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama

    def is_pendaftaran_aktif(self):
        if not self.periode_pendaftaran_mulai or not self.periode_pendaftaran_selesai:
            return False
        today = datetime.now().date()
        return self.periode_pendaftaran_mulai <= today <= self.periode_pendaftaran_selesai
    
    # Property to get berkas_dibutuhkan as a list
    @property
    def berkas_dibutuhkan(self):
        try:
            return json.loads(self.berkas_dibutuhkan_json)
        except (TypeError, json.JSONDecodeError):
            return []
    
    # Setter for berkas_dibutuhkan
    @berkas_dibutuhkan.setter
    def berkas_dibutuhkan(self, value):
        self.berkas_dibutuhkan_json = json.dumps(value)
    
    # Property to get alur_pendaftaran as a list
    @property
    def alur_pendaftaran(self):
        try:
            return json.loads(self.alur_pendaftaran_json)
        except (TypeError, json.JSONDecodeError):
            return []
    
    # Setter for alur_pendaftaran
    @alur_pendaftaran.setter
    def alur_pendaftaran(self, value):
        self.alur_pendaftaran_json = json.dumps(value)

class Mahasiswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mahasiswa')
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=20, unique=True)
    fakultas = models.CharField(max_length=50)
    angkatan = models.IntegerField()
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nama

class PendaftaranUKM(models.Model):
    STATUS_CHOICES = (
        ('diproses', 'Diproses'),
        ('diterima', 'Diterima'),
        ('ditolak', 'Ditolak'),
    )
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='pendaftaran_ukm')
    ukm = models.ForeignKey(UKM, on_delete=models.CASCADE)
    nomor_telepon = models.CharField(max_length=15, blank=True, null=True)
    foto_profil = models.ImageField(upload_to='pendaftar/foto_profil/', blank=True, null=True)
    dokumen_ktm = models.FileField(upload_to='pendaftar/dokumen_ktm/', blank=True, null=True)
    dokumen_cv = models.FileField(upload_to='pendaftar/dokumen_cv/', blank=True, null=True)
    dokumen_surat_minat = models.FileField(upload_to='pendaftar/dokumen_surat_minat/', blank=True, null=True)
    dokumen_lainnya = models.FileField(upload_to='pendaftar/dokumen_lainnya/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='diproses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mahasiswa.nama} - {self.ukm.nama}"

class Anggota(models.Model):
    ukm = models.ForeignKey(UKM, on_delete=models.CASCADE)
    pendaftaran = models.ForeignKey(PendaftaranUKM, on_delete=models.CASCADE)
    status_aktif = models.BooleanField(default=True)
    tanggal_bergabung = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.pendaftaran.mahasiswa.nama} - {self.ukm.nama}"

class Pesan(models.Model):
    pengirim = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pesan_dikirim')
    penerima = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pesan_diterima')  # Ubah ke User
    isi = models.TextField()
    tanggal_kirim = models.DateTimeField(auto_now_add=True)
    dibaca = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='balasan')

    def __str__(self):
        return f"Pesan dari {self.pengirim.username} ke {self.penerima.username}"