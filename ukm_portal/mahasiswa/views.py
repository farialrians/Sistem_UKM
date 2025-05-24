from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from admin_ukm.models import UKM, Mahasiswa, PendaftaranUKM, Anggota, Pesan
from .forms import MahasiswaRegistrationForm, PendaftaranUKMForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator


def register_mahasiswa(request):
    if request.method == 'POST':
        form = MahasiswaRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Mahasiswa.objects.create(
                user=user,
                nama=form.cleaned_data['nama'],
                nim=form.cleaned_data['npm'],
                email=form.cleaned_data['email'],
                fakultas=form.cleaned_data['fakultas'],
                angkatan=form.cleaned_data['angkatan']
            )
            messages.success(request, 'Registrasi berhasil. Silakan login.')
            return redirect('login_mahasiswa')
    else:
        form = MahasiswaRegistrationForm()
    return render(request, 'mahasiswa/register.html', {'form': form})

def login_mahasiswa(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_mahasiswa')
        else:
            messages.error(request, 'Username atau password salah.')
    return render(request, 'mahasiswa/login.html')

@login_required
def logout_mahasiswa(request):
    logout(request)
    messages.success(request, 'Anda telah berhasil logout.')
    return redirect('login_mahasiswa')

@login_required
def dashboard_mahasiswa(request):
    try:
        # Data mahasiswa
        mahasiswa = request.user.mahasiswa
        # Pendaftaran UKM
        pendaftaran = PendaftaranUKM.objects.filter(mahasiswa=mahasiswa)
        # Keanggotaan aktif
        anggota = Anggota.objects.filter(pendaftaran__mahasiswa=mahasiswa)
        # Pesan belum dibaca
        pesan_belum_dibaca = Pesan.objects.filter(penerima=request.user, dibaca=False).count()
        # Rekomendasi UKM (UKM yang sedang membuka pendaftaran dan belum didaftar oleh mahasiswa)
        rekomendasi_ukm = UKM.objects.filter(
            periode_pendaftaran_mulai__lte=timezone.now(),
            periode_pendaftaran_selesai__gte=timezone.now()
        ).exclude(
            id__in=pendaftaran.values_list('ukm__id', flat=True)
        )[:3]  # Batasi 3 rekomendasi
        # Aktivitas terbaru (pendaftaran terbaru dan pesan terbaru)
        aktivitas_pendaftaran = pendaftaran.order_by('-created_at')[:3]
        aktivitas_pesan = Pesan.objects.filter(penerima=request.user).order_by('-tanggal_kirim')[:3]
    except Mahasiswa.DoesNotExist:
        mahasiswa = None
        pendaftaran = None
        anggota = None
        pesan_belum_dibaca = 0
        rekomendasi_ukm = None
        aktivitas_pendaftaran = None
        aktivitas_pesan = None

    return render(request, 'mahasiswa/dashboard.html', {
        'mahasiswa': mahasiswa,
        'pendaftaran': pendaftaran,
        'anggota': anggota,
        'pesan_belum_dibaca': pesan_belum_dibaca,
        'rekomendasi_ukm': rekomendasi_ukm,
        'aktivitas_pendaftaran': aktivitas_pendaftaran,
        'aktivitas_pesan': aktivitas_pesan,
    })

@login_required
def profil_mahasiswa(request):
    try:
        mahasiswa = request.user.mahasiswa
    except Mahasiswa.DoesNotExist:
        messages.error(request, 'Data mahasiswa Anda tidak ditemukan. Silakan hubungi admin.')
        return redirect('dashboard_mahasiswa')
    return render(request, 'mahasiswa/profil.html', {'mahasiswa': mahasiswa})

@login_required
def pesan_mahasiswa(request):
    try:
        pesan_belum_dibaca = Pesan.objects.filter(penerima=request.user, dibaca=False).count()
        pesan = Pesan.objects.filter(penerima=request.user, parent__isnull=True).order_by('-tanggal_kirim')

        # Logika pencarian
        query = request.GET.get('q', '')
        if query:
            pesan = pesan.filter(
                Q(pengirim__username__icontains=query) | Q(isi__icontains=query)
            )
    except:
        pesan = None
        pesan_belum_dibaca = 0
        query = ''
    return render(request, 'mahasiswa/pesan.html', {
        'pesan': pesan,
        'pesan_belum_dibaca': pesan_belum_dibaca,
        'query': query
    })

@login_required
def detail_pesan(request, pesan_id):
    # Ambil pesan utama (parent is null) yang diterima oleh user ini
    # Atau pesan utama di mana user ini adalah pengirimnya (untuk melihat thread lengkap)
    pesan = get_object_or_404(
        Pesan,
        Q(id=pesan_id),
        Q(parent__isnull=True), # Pastikan ini adalah pesan utama thread
        Q(penerima=request.user) | Q(pengirim=request.user) # Pastikan user terlibat
    )

    # Tandai pesan utama dan semua balasannya yang ditujukan ke user ini sebagai dibaca
    if pesan.penerima == request.user and not pesan.dibaca:
        pesan.dibaca = True
        pesan.save()
    # Tandai balasan yang belum dibaca
    balasan_belum_dibaca = pesan.balasan.filter(penerima=request.user, dibaca=False)
    for balasan in balasan_belum_dibaca:
        balasan.dibaca = True
        balasan.save(update_fields=['dibaca']) # Lebih efisien

    # Ambil semua pesan dalam thread (pesan asli + semua balasan)
    # Urutkan berdasarkan tanggal kirim
    thread_pesan = list(pesan.balasan.all().order_by('tanggal_kirim'))
    thread_pesan.insert(0, pesan) # Masukkan pesan asli di awal

    # Tentukan siapa lawan bicara (admin)
    lawan_bicara = pesan.pengirim if pesan.penerima == request.user else pesan.penerima

    return render(request, 'mahasiswa/detail_pesan.html', {
        'pesan_asli': pesan, # Kirim pesan asli (parent) untuk konteks form
        'thread_pesan': thread_pesan, # Kirim semua pesan dalam thread
        'lawan_bicara': lawan_bicara # Kirim info admin
    })

@login_required
def balas_pesan(request, pesan_id):
    # Pesan yang dibalas adalah pesan PARENT/ASLI dari thread
    pesan_asli = get_object_or_404(Pesan, id=pesan_id, parent__isnull=True)

    # --- Pemeriksaan Keamanan ---
    # Pastikan user yang login adalah salah satu pihak dalam percakapan ini
    if not (pesan_asli.penerima == request.user or pesan_asli.pengirim == request.user):
         messages.error(request, "Anda tidak memiliki akses ke percakapan ini.")
         return redirect('pesan_mahasiswa')

    # Tentukan penerima balasan (lawan bicara)
    penerima_balasan = pesan_asli.pengirim if pesan_asli.penerima == request.user else pesan_asli.penerima

    if request.method == 'POST':
        isi_balasan = request.POST.get('isi_balasan')
        if isi_balasan:
            # Buat pesan balasan baru
            balasan_baru = Pesan.objects.create(
                pengirim=request.user,          # Pengirim adalah mahasiswa yang login
                penerima=penerima_balasan,      # Penerima adalah admin (lawan bicara)
                isi=isi_balasan,
                parent=pesan_asli               # Kaitkan ke pesan asli/thread
            )
            messages.success(request, f'Balasan berhasil dikirim kepada {penerima_balasan.username}.')

            # Kirim notifikasi ke admin (jika diperlukan, tambahkan logika Channels di sini)
            # Contoh:
            # channel_layer = get_channel_layer()
            # async_to_sync(channel_layer.group_send)(
            #     f'notifications_{penerima_balasan.id}', # Grup notifikasi admin
            #     {
            #         'type': 'send_notification',
            #         'message': {
            #             'pesan_id': balasan_baru.id,
            #             'pengirim': balasan_baru.pengirim.username,
            #             'isi': balasan_baru.isi,
            #             'tanggal_kirim': balasan_baru.tanggal_kirim.strftime('%Y-%m-%d %H:%M:%S'),
            #         }
            #     }
            # )

        else:
            messages.error(request, 'Isi balasan tidak boleh kosong.')
        # Selalu redirect kembali ke halaman detail pesan setelah POST
        return redirect('detail_pesan', pesan_id=pesan_asli.id)

    # Bagian GET request tidak lagi diperlukan jika form ada di detail_pesan
    # Anda bisa menghapus render 'mahasiswa/balas_pesan.html' atau biarkan saja
    # Redirect ke detail jika diakses via GET (lebih baik)
    messages.info(request, "Gunakan form di bawah untuk membalas.")
    return redirect('detail_pesan', pesan_id=pesan_asli.id)

@login_required
def tandai_dibaca(request, pesan_id):
    pesan = get_object_or_404(Pesan, id=pesan_id, penerima=request.user)
    pesan.dibaca = True
    pesan.save()
    messages.success(request, 'Pesan telah ditandai sebagai dibaca.')
    return redirect('detail_pesan', pesan_id=pesan_id)

@login_required
def hapus_pesan(request, pesan_id):
    pesan = get_object_or_404(Pesan, id=pesan_id, penerima=request.user)
    pesan.delete()
    messages.success(request, 'Pesan telah dihapus.')
    return redirect('pesan_mahasiswa')

@login_required
def list_ukm(request):
    # Ambil semua UKM
    ukms = UKM.objects.all()
    
    # Ambil query pencarian dari parameter GET
    query = request.GET.get('q', '')
    if query:
        ukms = ukms.filter(
            Q(nama__icontains=query) | Q(deskripsi__icontains=query)
        )
    
    # Ambil filter status pendaftaran
    status_filter = request.GET.get('status', 'all')
    now = timezone.now().date()  # Konversi ke datetime.date
    if status_filter == 'open':
        ukms = ukms.filter(
            periode_pendaftaran_mulai__lte=now,
            periode_pendaftaran_selesai__gte=now
        )
    
    # Pagination: Tampilkan 9 UKM per halaman
    paginator = Paginator(ukms, 9)  # 9 UKM per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Tambahkan status pendaftaran untuk setiap UKM di halaman saat ini
    for ukm in page_obj:
        ukm.is_open = (ukm.periode_pendaftaran_mulai <= now <= ukm.periode_pendaftaran_selesai)
    
    # Ambil data mahasiswa untuk navbar
    try:
        mahasiswa = request.user.mahasiswa
        pesan_belum_dibaca = Pesan.objects.filter(penerima=request.user, dibaca=False).count()
    except Mahasiswa.DoesNotExist:
        mahasiswa = None
        pesan_belum_dibaca = 0

    return render(request, 'mahasiswa/list_ukm.html', {
        'page_obj': page_obj,  # Kirim page_obj ke template, bukan ukms
        'query': query,
        'status_filter': status_filter,
        'mahasiswa': mahasiswa,
        'pesan_belum_dibaca': pesan_belum_dibaca,
    })

@login_required
def detail_ukm(request, ukm_id):
    ukm = get_object_or_404(UKM, id=ukm_id)
    return render(request, 'mahasiswa/detail_ukm.html', {'ukm': ukm})

@login_required
def daftar_ukm(request, ukm_id):
    ukm = get_object_or_404(UKM, id=ukm_id)
    
    if not ukm.is_pendaftaran_aktif():
        messages.error(request, 'Pendaftaran untuk UKM ini sudah ditutup.')
        return redirect('list_ukm')
    
    try:
        mahasiswa = request.user.mahasiswa
        if PendaftaranUKM.objects.filter(mahasiswa=mahasiswa, ukm=ukm).exists():
            messages.error(request, 'Anda sudah mendaftar ke UKM ini.')
            return redirect('dashboard_mahasiswa')
    except Mahasiswa.DoesNotExist:
        messages.error(request, 'Data mahasiswa Anda tidak ditemukan. Silakan hubungi admin.')
        return redirect('dashboard_mahasiswa')

    if request.method == 'POST':
        form = PendaftaranUKMForm(request.POST, request.FILES, ukm=ukm)
        if form.is_valid():
            pendaftaran = form.save(commit=False)
            pendaftaran.mahasiswa = mahasiswa
            pendaftaran.ukm = ukm
            pendaftaran.save()
            messages.success(request, 'Pendaftaran berhasil. Tunggu verifikasi dari admin UKM.')
            return redirect('dashboard_mahasiswa')
    else:
        form = PendaftaranUKMForm(ukm=ukm)
    return render(request, 'mahasiswa/daftar_ukm.html', {'form': form, 'ukm': ukm})

@login_required
def download_bukti_keanggotaan(request, anggota_id):
    anggota = get_object_or_404(Anggota, id=anggota_id, pendaftaran__mahasiswa=request.user.mahasiswa)
    
    if anggota.pendaftaran.mahasiswa != request.user.mahasiswa:
        messages.error(request, 'Anda tidak memiliki akses untuk mengunduh bukti keanggotaan ini.')
        return redirect('dashboard_mahasiswa')

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    title_style = styles['Heading1']
    title_style.alignment = 1
    elements.append(Paragraph("Bukti Keanggotaan UKM", title_style))
    elements.append(Spacer(1, 12))

    subtitle_style = styles['Heading3']
    subtitle_style.alignment = 1
    elements.append(Paragraph(f"Universitas [Nama Universitas]", subtitle_style))
    elements.append(Spacer(1, 24))

    normal_style = styles['Normal']
    normal_style.fontSize = 12
    normal_style.leading = 14

    elements.append(Paragraph(f"Nama: {anggota.pendaftaran.mahasiswa.nama}", normal_style))
    elements.append(Paragraph(f"NIM: {anggota.pendaftaran.mahasiswa.nim}", normal_style))
    elements.append(Paragraph(f"UKM: {anggota.ukm.nama}", normal_style))
    elements.append(Paragraph(f"Tanggal Bergabung: {anggota.tanggal_bergabung}", normal_style))
    elements.append(Paragraph(f"Status Keanggotaan: {'Aktif' if anggota.status_aktif else 'Tidak Aktif'}", normal_style))
    elements.append(Spacer(1, 24))

    elements.append(Paragraph("Dokumen ini dapat digunakan sebagai bukti keanggotaan untuk keperluan administrasi atau pendaftaran kegiatan UKM.", normal_style))
    elements.append(Spacer(1, 24))

    elements.append(Paragraph("Mengetahui,", normal_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Admin UKM", normal_style))
    elements.append(Paragraph(f"({anggota.ukm.admin_ukm.username})", normal_style))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bukti_keanggotaan_{anggota.pendaftaran.mahasiswa.nim}_{anggota.ukm.nama}.pdf"'
    response.write(pdf)
    return response