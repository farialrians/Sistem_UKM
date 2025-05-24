from django import forms
from admin_ukm.models import PendaftaranUKM
import phonenumbers
from phonenumbers import NumberParseException
from django.contrib.auth.models import User

# forms.py
class MahasiswaRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Konfirmasi Password')
    nama = forms.CharField(max_length=100, label='Nama Lengkap')
    npm = forms.CharField(max_length=20, label='NPM')
    email = forms.EmailField(label='Email')
    fakultas = forms.CharField(max_length=50, label='Fakultas')
    angkatan = forms.IntegerField(label='Angkatan')
    
    # Tambahkan validasi untuk memastikan password1 dan password2 sama
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Password tidak cocok")
            
        return cleaned_data
    
    # Perbarui metode save untuk menggunakan password1
    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password1']  # Gunakan password1 di sini
        )
        return user

class PendaftaranUKMForm(forms.ModelForm):
    nomor_telepon = forms.CharField(max_length=15, required=False, label='Nomor Telepon')
    foto_profil = forms.ImageField(required=False, label='Foto Profil')
    dokumen_ktm = forms.FileField(required=False, label='KTM')
    dokumen_cv = forms.FileField(required=False, label='CV')
    dokumen_surat_minat = forms.FileField(required=False, label='Surat Minat')
    dokumen_lainnya = forms.FileField(required=False, label='Dokumen Lainnya')

    class Meta:
        model = PendaftaranUKM
        fields = ['nomor_telepon', 'foto_profil', 'dokumen_ktm', 'dokumen_cv', 'dokumen_surat_minat', 'dokumen_lainnya']

    def __init__(self, *args, **kwargs):
        self.ukm = kwargs.pop('ukm', None)
        super().__init__(*args, **kwargs)
        if self.ukm:
            required_docs = self.ukm.berkas_dibutuhkan
            if 'ktm' in required_docs:
                self.fields['dokumen_ktm'].required = True
            if 'cv' in required_docs:
                self.fields['dokumen_cv'].required = True
            if 'surat_minat' in required_docs:
                self.fields['dokumen_surat_minat'].required = True
            if 'lainnya' in required_docs:
                self.fields['dokumen_lainnya'].required = True

    def clean_nomor_telepon(self):
        nomor_telepon = self.cleaned_data.get('nomor_telepon')
        if nomor_telepon:
            try:
                # Parse nomor telepon
                parsed_number = phonenumbers.parse(nomor_telepon, None)
                # Validasi nomor telepon
                if not phonenumbers.is_valid_number(parsed_number):
                    raise forms.ValidationError("Nomor telepon tidak valid. Gunakan format internasional, misalnya: +6281234567890")
                # Format nomor telepon ke format internasional
                formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
                return formatted_number
            except NumberParseException:
                raise forms.ValidationError("Nomor telepon tidak valid. Gunakan format internasional, misalnya: +6281234567890")
        return nomor_telepon