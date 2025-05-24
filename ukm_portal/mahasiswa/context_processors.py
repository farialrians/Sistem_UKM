from admin_ukm.models import Pesan

def pesan_belum_dibaca(request):
    if request.user.is_authenticated:
        try:
            pesan_belum_dibaca = Pesan.objects.filter(penerima=request.user, dibaca=False).count()
        except:
            pesan_belum_dibaca = 0
    else:
        pesan_belum_dibaca = 0
    return {
        'pesan_belum_dibaca': pesan_belum_dibaca,
    }