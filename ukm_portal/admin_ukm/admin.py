from django.contrib import admin
from .models import UKM, Mahasiswa, PendaftaranUKM, Anggota

@admin.register(UKM)
class UKMAdmin(admin.ModelAdmin):
    list_display = ('nama', 'admin_ukm', 'created_at')
    list_filter = ('jenis_kegiatan', 'created_at')
    search_fields = ('nama',)

@admin.register(Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nim', 'email', 'fakultas', 'angkatan')
    search_fields = ('nama', 'nim', 'email')

@admin.register(PendaftaranUKM)
class PendaftaranUKMAdmin(admin.ModelAdmin):
    list_display = ('mahasiswa', 'ukm', 'status', 'created_at')
    list_filter = ('status', 'ukm', 'created_at')
    search_fields = ('mahasiswa__nama', 'ukm__nama')

@admin.register(Anggota)
class AnggotaAdmin(admin.ModelAdmin):
    list_display = ('pendaftaran', 'ukm', 'status_aktif', 'tanggal_bergabung')
    list_filter = ('status_aktif', 'ukm')
    search_fields = ('pendaftaran__mahasiswa__nama', 'ukm__nama')