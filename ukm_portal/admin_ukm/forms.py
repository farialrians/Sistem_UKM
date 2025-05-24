from django import forms
from django.core.exceptions import ValidationError
from .models import UKM
from tinymce.widgets import TinyMCE

class UKMForm(forms.ModelForm):
    # Gunakan TinyMCE widget untuk field teks
    deskripsi_singkat = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    visi = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    misi = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    persyaratan_umum = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    
    # Field untuk berkas dan alur pendaftaran
    berkas_dibutuhkan = forms.MultipleChoiceField(
        choices=UKM.BERKAS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        error_messages={'required': 'Harap pilih setidaknya satu berkas yang dibutuhkan.'}
    )
    
    alur_pendaftaran = forms.MultipleChoiceField(
        choices=UKM.ALUR_PENDAFTARAN_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        error_messages={'required': 'Harap pilih setidaknya satu alur pendaftaran.'}
    )
    
    # Widget time input
    waktu_mulai = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control time-picker'}),
        required=True,
        error_messages={'required': 'Harap masukkan waktu mulai kegiatan.'}
    )
    
    waktu_selesai = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control time-picker'}),
        required=True,
        error_messages={'required': 'Harap masukkan waktu selesai kegiatan.'}
    )

    # Widget untuk periode pendaftaran
    periode_pendaftaran_mulai = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        label="Tanggal Mulai Pendaftaran"
    )
    periode_pendaftaran_selesai = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        label="Tanggal Selesai Pendaftaran"
    )
    
    class Meta:
        model = UKM
        exclude = ['admin_ukm', 'created_at', 'berkas_dibutuhkan_json', 'alur_pendaftaran_json']
        error_messages = {
            'nama': {'required': 'Nama UKM wajib diisi.'},
            'deskripsi_singkat': {'required': 'Deskripsi singkat wajib diisi.'},
            'visi': {'required': 'Visi wajib diisi.'},
            'misi': {'required': 'Misi wajib diisi.'},
            'jenis_kegiatan': {'required': 'Harap pilih jenis kegiatan.'},
            'hari_mulai': {'required': 'Harap pilih hari mulai kegiatan.'},
            'hari_selesai': {'required': 'Harap pilih hari selesai kegiatan.'},
            'ketua_ukm': {'required': 'Nama ketua UKM wajib diisi.'},
            'pengurus_pendaftaran': {'required': 'Nama pengurus pendaftaran wajib diisi.'},
            'persyaratan_umum': {'required': 'Persyaratan umum wajib diisi.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Use the property to get the list values
            self.initial['berkas_dibutuhkan'] = self.instance.berkas_dibutuhkan
            self.initial['alur_pendaftaran'] = self.instance.alur_pendaftaran
    
    def clean(self):
        cleaned_data = super().clean()
        # Validasi waktu kegiatan
        waktu_mulai = cleaned_data.get('waktu_mulai')
        waktu_selesai = cleaned_data.get('waktu_selesai')
        if waktu_mulai and waktu_selesai and waktu_mulai >= waktu_selesai:
            raise ValidationError("Waktu mulai harus lebih awal dari waktu selesai.")

        # Validasi periode pendaftaran
        periode_mulai = cleaned_data.get('periode_pendaftaran_mulai')
        periode_selesai = cleaned_data.get('periode_pendaftaran_selesai')
        if periode_mulai and periode_selesai:
            if periode_mulai > periode_selesai:
                raise ValidationError("Tanggal mulai pendaftaran harus lebih awal dari tanggal selesai.")
        elif periode_mulai and not periode_selesai:
            raise ValidationError("Harap masukkan tanggal selesai pendaftaran.")
        elif periode_selesai and not periode_mulai:
            raise ValidationError("Harap masukkan tanggal mulai pendaftaran.")
        
        return cleaned_data

    def save(self, commit=True):
        ukm = super().save(commit=False)
        # Use the property setter
        ukm.berkas_dibutuhkan = self.cleaned_data.get('berkas_dibutuhkan', [])
        ukm.alur_pendaftaran = self.cleaned_data.get('alur_pendaftaran', [])
        if commit:
            ukm.save()
        return ukm