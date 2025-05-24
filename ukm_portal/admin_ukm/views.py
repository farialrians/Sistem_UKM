from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UKM, PendaftaranUKM, Anggota, Pesan, Mahasiswa
from .forms import UKMForm  
from django.contrib.auth import logout
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q, Max, OuterRef, Subquery, Exists, Value, BooleanField 
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.contrib.auth.models import User

@login_required
def view_or_start_conversation(request, target_user_id):
    if not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
        return redirect('login')  

    admin_user = request.user
    target_user = get_object_or_404(User, id=target_user_id)

    if admin_user == target_user:
        messages.warning(request, "Anda tidak dapat memulai percakapan dengan diri sendiri.")
        return redirect(request.META.get('HTTP_REFERER', 'admin_dashboard'))
    try:
        ukm_admin = admin_user.ukm_set.first()
        if not ukm_admin:
            raise UKM.DoesNotExist

        is_related = PendaftaranUKM.objects.filter(
            mahasiswa__user=target_user,
            ukm=ukm_admin
        ).exists()

        if not is_related:
            messages.error(request, f"Anda tidak dapat memulai percakapan dengan pengguna ini karena tidak terkait dengan {ukm_admin.nama}.")
            return redirect(request.META.get('HTTP_REFERER', 'admin_dashboard'))

    except UKM.DoesNotExist:
        messages.error(request, "Anda tidak terhubung dengan UKM manapun.")
        return redirect('admin_dashboard')
    except Exception as e:
        messages.error(request, f"Terjadi kesalahan keamanan: {e}")
        return redirect('admin_dashboard')

    existing_thread = Pesan.objects.filter(
        parent__isnull=True
    ).filter(
        (Q(pengirim=admin_user) & Q(penerima=target_user)) |
        (Q(pengirim=target_user) & Q(penerima=admin_user))
    ).first()
    if existing_thread:
        return redirect('balas_pesan_admin', pesan_id=existing_thread.id)
    else:
        new_thread = Pesan.objects.create(
            pengirim=admin_user,
            penerima=target_user,
            isi=f"[Percakapan dimulai antara {admin_user.username} dan {target_user.username}]", # Placeholder
            parent=None
        )
        messages.info(request, f"Memulai percakapan baru dengan {target_user.get_full_name() or target_user.username}.")
        return redirect('balas_pesan_admin', pesan_id=new_thread.id)

@login_required
def balas_pesan_admin(request, pesan_id):
    if not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
        return redirect('halaman_mahasiswa')  # Ganti dengan URL halaman mahasiswa

    try:
        pesan_utama = Pesan.objects.get(id=pesan_id, parent__isnull=True)
    except Pesan.DoesNotExist:
        messages.error(request, "Percakapan tidak ditemukan.")
        return redirect('semua_pesan')

    if not (pesan_utama.pengirim == request.user or pesan_utama.penerima == request.user):
        messages.error(request, "Anda tidak memiliki akses ke percakapan ini.")
        return redirect('semua_pesan')

    if request.method == 'POST':
        isi_balasan = request.POST.get('isi_balasan')
        if isi_balasan:
            penerima_balasan = pesan_utama.pengirim if pesan_utama.penerima == request.user else pesan_utama.penerima
            balasan_baru = Pesan.objects.create(
                pengirim=request.user,
                penerima=penerima_balasan,
                isi=isi_balasan,
                parent=pesan_utama
            )
            messages.success(request, f'Balasan berhasil dikirim kepada {penerima_balasan.username}.')

            return redirect('balas_pesan_admin', pesan_id=pesan_utama.id)
        else:
            messages.error(request, 'Isi balasan tidak boleh kosong.')
            return redirect('balas_pesan_admin', pesan_id=pesan_utama.id)

    pesan_thread_belum_dibaca = Pesan.objects.filter(
        (Q(id=pesan_utama.id) | Q(parent=pesan_utama)),
        penerima=request.user,
        dibaca=False
    )
    for p in pesan_thread_belum_dibaca:
        p.dibaca = True
        p.save(update_fields=['dibaca'])

    thread_pesan = list(pesan_utama.balasan.all().order_by('tanggal_kirim'))
    thread_pesan.insert(0, pesan_utama)

    lawan_bicara = pesan_utama.pengirim if pesan_utama.penerima == request.user else pesan_utama.penerima

    context = {
        'pesan_asli': pesan_utama,
        'thread_pesan': thread_pesan,
        'lawan_bicara': lawan_bicara,
    }
    return render(request, 'admin_ukm/balas_pesan.html', context)

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
        return redirect('login')  # Ganti dengan URL halaman mahasiswa

    ukm = None
    pending_registrations_count = 0
    total_members_count = 0
    unread_messages_count = 0
    try:
        ukm = UKM.objects.get(admin_ukm=request.user)
        pending_registrations_count = PendaftaranUKM.objects.filter(
            ukm=ukm,
            status='diproses'
        ).count()
        total_members_count = Anggota.objects.filter(
            ukm=ukm,
            status_aktif=True
        ).count()
        unread_messages_count = Pesan.objects.filter(
            penerima=request.user,
            dibaca=False

        ).count()

    except UKM.DoesNotExist:
        pass
    except Exception as e:
        messages.error(request, f"Terjadi kesalahan saat memuat data dashboard: {e}")

    context = {
        'ukm': ukm,
        'pending_registrations_count': pending_registrations_count,
        'total_members_count': total_members_count,
        'unread_messages_count': unread_messages_count,
    }
    return render(request, 'admin_ukm/dashboard.html', context)

@login_required
def upload_ukm_info(request):
    if not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
        return redirect('login')  # Ganti dengan URL halaman mahasiswa

    ukm = None  # Inisialisasi ukm di luar blok try
    try:
        ukm = UKM.objects.get(admin_ukm=request.user)
    except UKM.DoesNotExist:
        pass # ukm tetap None jika tidak ditemukan

    if request.method == 'POST':
        form = UKMForm(request.POST, request.FILES, instance=ukm)
        if form.is_valid():
            ukm = form.save(commit=False)
            ukm.admin_ukm = request.user  # Selalu set admin_ukm ke user yang login
            ukm.save()
            messages.success(request, 'Informasi UKM berhasil diperbarui.')
            return redirect('admin_dashboard')
    else:
        form = UKMForm(instance=ukm)

    return render(request, 'admin_ukm/upload_ukm_info.html', {'form': form})

@login_required
def view_pendaftar(request):
    if not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
        return redirect('login')  # Ganti dengan URL halaman mahasiswa

    try:
        ukm = UKM.objects.get(admin_ukm=request.user)
        pendaftar = PendaftaranUKM.objects.filter(ukm=ukm)

        pendaftar_menunggu = pendaftar.filter(status='diproses')
        pendaftar_diterima = pendaftar.filter(status='diterima')
        pendaftar_ditolak = pendaftar.filter(status='ditolak')

        query = request.GET.get('q')
        if query:
            pendaftar_menunggu = pendaftar_menunggu.filter(
                Q(mahasiswa__nama__icontains=query) |
                Q(mahasiswa__nim__icontains=query)
            )
            pendaftar_diterima = pendaftar_diterima.filter(
                Q(mahasiswa__nama__icontains=query) |
                Q(mahasiswa__nim__icontains=query)
            )
            pendaftar_ditolak = pendaftar_ditolak.filter(
                Q(mahasiswa__nama__icontains=query) |
                Q(mahasiswa__nim__icontains=query)
            )

    except UKM.DoesNotExist:
        ukm = None
        pendaftar_menunggu = None
        pendaftar_diterima = None
        pendaftar_ditolak = None

    return render(request, 'admin_ukm/view_pendaftar.html', {
        'ukm': ukm,
        'pendaftar_menunggu': pendaftar_menunggu,
        'pendaftar_diterima': pendaftar_diterima,
        'pendaftar_ditolak': pendaftar_ditolak,
    })

@login_required
def verify_pendaftar(request, pendaftar_id):
    if not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
        return redirect('login')

    pendaftar = get_object_or_404(PendaftaranUKM, id=pendaftar_id)
    if pendaftar.ukm.admin_ukm != request.user:
        messages.error(request, 'Anda tidak memiliki akses untuk memverifikasi pendaftar ini.')
        return redirect('view_pendaftar')

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['diterima', 'ditolak']:
            pendaftar.status = status
            pendaftar.save()
            if status == 'diterima':
                Anggota.objects.create(
                    ukm=pendaftar.ukm,
                    pendaftaran=pendaftar,
                    status_aktif=True
                )
            messages.success(request, f'Pendaftar telah {status}.')
            return redirect('view_pendaftar')
        else:
            messages.error(request, 'Status tidak valid.')
            return redirect('view_pendaftar')

    # Untuk GET request, render halaman detail
    context = {
        'pendaftar': pendaftar,
    }
    return render(request, 'admin_ukm/verify_pendaftar.html', context)

@login_required
def hapus_pesan_admin(request, pesan_id):
    if not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
        return redirect('halaman_mahasiswa')  # Ganti dengan URL halaman mahasiswa

    pesan = get_object_or_404(Pesan, id=pesan_id, pengirim=request.user)
    pesan.delete()
    messages.success(request, 'Pesan telah dihapus.')
    return redirect('admin_dashboard')

@login_required
def semua_pesan(request):
    if not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
        return redirect('login')  # Ganti dengan URL halaman mahasiswa

    user = request.user

    # 1. Dapatkan semua ID pesan utama (parent) di mana admin terlibat
    thread_ids = Pesan.objects.filter(
        parent__isnull=True
    ).filter(
        Q(pengirim=user) | Q(penerima=user)
    ).values_list('id', flat=True)

    # 2. Dapatkan QuerySet utama berdasarkan ID thread
    threads = Pesan.objects.filter(id__in=thread_ids)

    # 3. Annotate dengan informasi pesan terakhir dalam setiap thread
    last_message_subquery = Pesan.objects.filter(
        # Pesan adalah parent (OuterRef('pk')) ATAU balasan dari parent tsb
        Q(id=OuterRef('pk')) | Q(parent_id=OuterRef('pk'))
    ).order_by('-tanggal_kirim') # Urutkan dari terbaru

    threads = threads.annotate(
        # Ambil ID pesan terakhir
        last_message_id=Subquery(last_message_subquery.values('id')[:1]),
        # Ambil isi pesan terakhir
        last_message_isi=Subquery(last_message_subquery.values('isi')[:1]),
        # Ambil waktu pesan terakhir
        last_message_time=Subquery(last_message_subquery.values('tanggal_kirim')[:1])
    )

    # 4. Annotate apakah thread memiliki pesan belum dibaca UNTUK admin
    unread_subquery = Pesan.objects.filter(
        (Q(id=OuterRef('pk')) | Q(parent_id=OuterRef('pk'))), # Pesan dalam thread
        penerima=user,
        dibaca=False
    )
    threads = threads.annotate(
        has_unread=Exists(unread_subquery)
    )

    # 5. Urutkan thread berdasarkan waktu pesan terakhir
    threads = threads.order_by(Coalesce('last_message_time', 'tanggal_kirim').desc()) # Urutkan descending

    # 6. Fitur Pencarian (Opsional tapi bagus)
    query = request.GET.get('q')
    if query:
        # Cari berdasarkan nama/username pengirim/penerima ATAU isi pesan terakhir
        threads = threads.filter(
            Q(pengirim__username__icontains=query) |
            Q(penerima__username__icontains=query) |
            Q(pengirim__first_name__icontains=query) |
            Q(penerima__first_name__icontains=query) |
            Q(pengirim__last_name__icontains=query) |
            Q(penerima__last_name__icontains=query) |
            Q(last_message_isi__icontains=query) # Cari di pesan terakhir
        ).distinct() # Gunakan distinct jika join/filter bisa menghasilkan duplikat

    # 7. Tandai pesan sebagai dibaca (jika user membuka halaman ini)
    # Jika Anda ingin menandai *semua* pesan sebagai dibaca saat halaman ini dibuka:
    # Pesan.objects.filter(penerima=user, dibaca=False).update(dibaca=True)
    # Namun, ini mungkin kurang ideal. Lebih baik menandai saat detail dibuka.
    # Biarkan penghitungan di context processor yang menghitung unread.

    context = {
        'threads': threads,
        'query': query,
        # 'unread_messages_count_admin' akan datang dari context processor
    }
    return render(request, 'admin_ukm/semua_pesan.html', context)

@login_required
def view_anggota(request):
    if not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
        return redirect('login')  # Ganti dengan URL halaman mahasiswa

    anggota_qs = Anggota.objects.none() # Default queryset kosong
    ukm = None

    try:
        ukm = UKM.objects.get(admin_ukm=request.user)

        # Queryset dasar: anggota UKM ini, optimalkan dengan select_related
        anggota_qs = Anggota.objects.filter(ukm=ukm).select_related(
            'pendaftaran__mahasiswa' # Ambil data mahasiswa terkait dalam 1 query
        ).order_by('pendaftaran__mahasiswa__nama') # Urutkan berdasarkan nama

        # Ambil parameter GET
        query = request.GET.get('q')
        status_filter = request.GET.get('status')

        # --- Terapkan Filter Pencarian ---
        if query:
            anggota_qs = anggota_qs.filter(
                Q(pendaftaran__mahasiswa__nama__icontains=query) |
                Q(pendaftaran__mahasiswa__nim__icontains=query)
            )

        # --- Terapkan Filter Status ---
        if status_filter == 'aktif':
            anggota_qs = anggota_qs.filter(status_aktif=True)
        elif status_filter == 'tidak_aktif':
            anggota_qs = anggota_qs.filter(status_aktif=False)
        # Jika status_filter kosong atau tidak valid, tidak perlu filter status tambahan

    except UKM.DoesNotExist:
        messages.warning(request, "Anda belum terdaftar sebagai admin UKM.")
        # Biarkan anggota_qs kosong
    except Exception as e:
        messages.error(request, f"Terjadi kesalahan saat memuat data anggota: {e}")
        anggota_qs = Anggota.objects.none() # Kosongkan jika error

    context = {
        'anggota': anggota_qs, # Kirim queryset yang SUDAH DIFILTER
        'ukm': ukm
        # 'query' dan 'status_filter' tidak perlu dikirim ke context
        # karena template sudah mengambilnya dari request.GET
    }
    return render(request, 'admin_ukm/view_anggota.html', context)

@login_required
def manage_anggota(request, anggota_id):
    if not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
        return redirect('login')  # Ganti dengan URL halaman mahasiswa

    anggota = get_object_or_404(Anggota, id=anggota_id)
    if anggota.ukm.admin_ukm != request.user:
        messages.error(request, 'Anda tidak memiliki akses untuk mengelola anggota ini.')
        return redirect('view_anggota')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'toggle_status':
            status_aktif_baru = request.POST.get('status_aktif') == 'on'
            if anggota.status_aktif != status_aktif_baru:
                anggota.status_aktif = status_aktif_baru
                anggota.save()
                messages.success(request, f'Status anggota "{anggota.pendaftaran.mahasiswa.nama}" telah diperbarui.')
            current_query_params = request.GET.urlencode()
            redirect_url = f"{reverse('view_anggota')}?{current_query_params}"
            return redirect(redirect_url)


        elif action == 'hapus':
            nama_anggota = anggota.pendaftaran.mahasiswa.nama
            anggota.delete()
            messages.success(request, f'Anggota "{nama_anggota}" telah dihapus dari UKM.')
            current_query_params = request.GET.urlencode()
            redirect_url = f"{reverse('view_anggota')}?{current_query_params}"
            return redirect(redirect_url)

        else:
            messages.warning(request, 'Aksi tidak dikenali.')

            current_query_params = request.GET.urlencode()
            redirect_url = f"{reverse('view_anggota')}?{current_query_params}"
            return redirect(redirect_url)

    context = {
        'anggota': anggota,
        'ukm': anggota.ukm
    }
    return render(request, 'admin_ukm/manage_anggota_detail.html', context)

def custom_logout(request):
    logout(request)
    messages.success(request, 'Anda telah berhasil logout.')
    return redirect('login')