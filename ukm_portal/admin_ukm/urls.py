from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('upload-ukm-info/', views.upload_ukm_info, name='upload_ukm_info'),
    path('pendaftar/', views.view_pendaftar, name='view_pendaftar'),
    path('verify/<int:pendaftar_id>/', views.verify_pendaftar, name='verify_pendaftar'),
    path('anggota/', views.view_anggota, name='view_anggota'),
    path('anggota/<int:anggota_id>/manage/', views.manage_anggota, name='manage_anggota'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('pesan/<int:pesan_id>/balas/', views.balas_pesan_admin, name='balas_pesan_admin'),
    path('pesan/<int:pesan_id>/hapus/', views.hapus_pesan_admin, name='hapus_pesan_admin'),
    path('semua-pesan/', views.semua_pesan, name='semua_pesan'),
    path('percakapan/user/<int:target_user_id>/', views.view_or_start_conversation, name='view_or_start_conversation'),
]