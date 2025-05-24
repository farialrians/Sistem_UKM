from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .models import UKM, Pendaftar, Anggota
from .forms import UKMForm
from django.core.mail import send_mail
from django.conf import settings

@login_required
def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    ukm = UKM.objects.filter(admin_ukm=request.user).first()
    return render(request, 'admin_ukm/dashboard.html', {'ukm': ukm})

@login_required
def upload_ukm_info(request):
    ukm = UKM.objects.filter(admin_ukm=request.user).first()
    if request.method == 'POST':
        form = UKMForm(request.POST, request.FILES, instance=ukm)
        if form.is_valid():
            ukm = form.save(commit=False)
            ukm.admin_ukm = request.user
            ukm.save()
            messages.success(request, 'Informasi UKM berhasil diperbarui.')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Harap perbaiki kesalahan di bawah ini.')
    else:
        form = UKMForm(instance=ukm)
    return render(request, 'admin_ukm/upload_ukm_info.html', {'form': form})

@login_required
def view_pendaftar(request):
    ukm = UKM.objects.filter(admin_ukm=request.user).first()
    if not ukm:
        messages.error(request, 'Anda belum mengelola UKM.')
        return redirect('admin_dashboard')
    pendaftar_list = Pendaftar.objects.filter(ukm=ukm)
    return render(request, 'admin_ukm/view_pendaftar.html', {'pendaftar_list': pendaftar_list, 'ukm': ukm})

@login_required
def verify_pendaftar(request, pendaftar_id):
    pendaftar = get_object_or_404(Pendaftar, id=pendaftar_id)
    ukm = UKM.objects.filter(admin_ukm=request.user).first()
    if pendaftar.ukm != ukm:
        messages.error(request, 'Anda tidak memiliki akses untuk memverifikasi pendaftar ini.')
        return redirect('view_pendaftar')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'terima' and pendaftar.status == 'diproses':
            pendaftar.status = 'diterima'
            pendaftar.save()
            Anggota.objects.create(ukm=pendaftar.ukm, pendaftar=pendaftar)
            # Kirim notifikasi email menggunakan email pendaftar
            send_mail(
                'Selamat, Anda Diterima di UKM!',
                f'Halo {pendaftar.nama},\n\nSelamat, Anda telah diterima di {pendaftar.ukm.nama}. Silakan hubungi pengurus untuk informasi lebih lanjut.\n\nSalam,\nTim UKM',
                settings.EMAIL_HOST_USER,
                [pendaftar.email],  # Gunakan email pendaftar
                fail_silently=False,
            )
            messages.success(request, f'{pendaftar.nama} berhasil diterima.')
        elif action == 'tolak' and pendaftar.status == 'diproses':
            pendaftar.status = 'ditolak'
            pendaftar.save()
            send_mail(
                'Status Pendaftaran UKM',
                f'Halo {pendaftar.nama},\n\nMohon maaf, Anda tidak diterima di {pendaftar.ukm.nama}. Terima kasih atas minat Anda.\n\nSalam,\nTim UKM',
                settings.EMAIL_HOST_USER,
                [pendaftar.email],  # Gunakan email pendaftar
                fail_silently=False,
            )
            messages.success(request, f'{pendaftar.nama} telah ditolak.')
        return redirect('view_pendaftar')
    return render(request, 'admin_ukm/verify_pendaftar.html', {'pendaftar': pendaftar})

@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, 'Anda telah berhasil logout.')
    return redirect('login')