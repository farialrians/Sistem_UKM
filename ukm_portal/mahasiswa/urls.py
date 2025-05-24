from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_mahasiswa, name='register_mahasiswa'),
    path('login/', views.login_mahasiswa, name='login_mahasiswa'),
    path('logout/', views.logout_mahasiswa, name='logout_mahasiswa'),
    path('dashboard/', views.dashboard_mahasiswa, name='dashboard_mahasiswa'),
    path('ukm/', views.list_ukm, name='list_ukm'),
    path('ukm/<int:ukm_id>/', views.detail_ukm, name='detail_ukm'),
    path('ukm/<int:ukm_id>/daftar/', views.daftar_ukm, name='daftar_ukm'),
    path('bukti-keanggotaan/<int:anggota_id>/download/', views.download_bukti_keanggotaan, name='download_bukti_keanggotaan'),
    path('pesan/<int:pesan_id>/tandai-dibaca/', views.tandai_dibaca, name='tandai_dibaca'),
    path('pesan/<int:pesan_id>/hapus/', views.hapus_pesan, name='hapus_pesan'),
    path('pesan/<int:pesan_id>/balas/', views.balas_pesan, name='balas_pesan'),
    path('profil/', views.profil_mahasiswa, name='profil_mahasiswa'),
    path('pesan/', views.pesan_mahasiswa, name='pesan_mahasiswa'),
    path('pesan/<int:pesan_id>/', views.detail_pesan, name='detail_pesan'),
]