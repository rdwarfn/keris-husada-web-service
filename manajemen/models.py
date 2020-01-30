from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

# from django.contrib.auth.validators import UnicodeUsernameValidator

from manajemen.manager import MyUserManager

class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    # username_validator = UnicodeUsernameValidator()

    USER_TYPE = (
        (1, 'Mahasiswa'),
        (2, 'Dosen'),
        (3, 'Admin'),
    )
    
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        # validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=True)
    phone_number = PhoneNumberField(
        _('phone number'),
        blank=True
    )
    user_type = models.PositiveSmallIntegerField(_('user'), choices=USER_TYPE)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_joined = models.DateTimeField(
        _('date joined'), 
        auto_now_add=True
    )

    objects = MyUserManager()

    # EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['user_type']

    class Meta:
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        '''Send mail to this user.'''
        send_mail(subject, message, from_mail, [self.email], **kwargs)


from django.utils.text import slugify
from django.conf import settings
from datetime import date


AGAMA = [
    ('buddha', 'Buddha'),
    ('hindu', 'Hindu'),
    ('islam', 'Islam'),
    ('konghucu', 'Kong Hu Cu'),
    ('Kristen',(
        ('katolik', 'Katolik'),
        ('protestan', 'Protestan'),
    )),
]

JENIS_KELAMIN = [
    ('L', 'Laki-laki'),
    ('P', 'Perempuan'),
]

HUBUNGAN = [
    ('Ayah', 'Ayah'),
    ('Ibu', 'Ibu'),
    ('Lainnya', 'Lainnya'),
]

def checkNone(args):
    if args is not None:
        return args.title()
    else:
        return

def YEAR_CHOICES():
    return [(y,y) for y in range(2016, date.today().year + 20)]

def SMT_MASUK():
    return [
        (str(a), (
            (a, '{} Genap'.format(a)),
            (a + 0.5, '{} Ganjil'.format(a))
            )
        ) for a in range(2016, date.today().year + 20)
    ]

def CURRENT_YEAR():
    return date.today().year


class Angkatan(models.Model):
    tahun   = models.PositiveIntegerField('Tahun Angkatan')
    semester= models.CharField(max_length=6, choices=[('Genap', 'Genap'), ('Ganjil', 'Ganjil')])

    def __str__(self):
        return '{} - {}'.format(self.tahun, self.semester)
    
    class Meta:
        verbose_name_plural = 'Angkatan'
        verbose_name = 'Data angkatan'


class Mahasiswa(models.Model):
    """Profil Mahasiswa"""
    akun            = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, help_text='digunakan untuk login SIA', related_name='akun_mahasiswa')
    nim             = models.CharField(primary_key=True, verbose_name='NIM', max_length=9, help_text='nomor induk mahasiswa')
    nama_lengkap    = models.CharField(max_length=225)
    jenis_kelamin   = models.CharField(max_length=1, choices=JENIS_KELAMIN)
    gol_darah       = models.CharField(max_length=2, choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], null=True, blank=True)
    kewarganegaraan = models.CharField(max_length=3, choices=[('WNI', 'WNI'), ('WNA', 'WNA')], default='WNI')
    tempat_lahir    = models.CharField(max_length=40)
    tanggal_lahir   = models.DateField()
    agama           = models.CharField(max_length=9, choices=AGAMA, default='islam')
    alamat          = models.TextField(help_text='nama jalan, nomor rumah', null=True, blank=True)
    rt              = models.PositiveSmallIntegerField(help_text='rukun tetangga', verbose_name='RT', null=True, blank=True)
    rw              = models.PositiveSmallIntegerField(help_text='rukun warga', verbose_name='RW', null=True, blank=True)
    kelurahan       = models.CharField(max_length=30, verbose_name='Kelurahan / Desa', null=True, blank=True)
    kecamatan       = models.CharField(max_length=30, null=True, blank=True)
    kab_kota        = models.CharField(max_length=30, verbose_name='Kabupaten / Kota', null=True, blank=True)
    provinsi        = models.CharField(max_length=30, null=True, blank=True)
    kode_pos        = models.PositiveSmallIntegerField(null=True, blank=True)
    nomor_telepon   = PhoneNumberField(help_text='No. Telp. Rumah', null=True, blank=True)
    nomor_handphone = PhoneNumberField(help_text='No. Handphone', null=True, blank=True)
    ktp             = models.CharField(max_length=16, null=True, blank=True)
    email           = models.EmailField(null=True, blank=True)
    program_studi   = models.ForeignKey('akademik.ProgramStudi', null=True, on_delete=models.SET_NULL, related_name='program_studi_mahasiswa')
    status_awal     = models.CharField(max_length=8, choices=[('Baru', 'Baru'), ('Pindahan', 'Pindahan')], default='Baru')
    angkatan        = models.ForeignKey('Angkatan', null=True, on_delete=models.CASCADE)
    tahun_semester_masuk  = models.FloatField(
        choices=SMT_MASUK(),
        null=True,
        blank=True,
    )
    tanggal_masuk   = models.DateField()
    status          = models.CharField(choices=[('Aktif', 'Aktif'), ('Lulus', 'Lulus'), ('DO', 'Drop Out')], max_length=5, default='Aktif')
    file_foto       = models.ImageField(upload_to='mahasiswa/foto/', blank=True)
    slug            = models.SlugField(blank=True, editable=False)
    dibuat_pada     = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.nama_lengkap   = self.nama_lengkap.title()
        self.tempat_lahir   = checkNone(self.tempat_lahir)
        self.kelurahan      = checkNone(self.kelurahan)
        self.kecamatan      = checkNone(self.kecamatan)
        self.kab_kota       = checkNone(self.kab_kota)
        self.kewarganegaraan= checkNone(self.kewarganegaraan)
        self.email          = self.akun.email if self.akun else None
        self.nomor_handphone= self.akun.phone_number if self.akun else None
        self.slug           = slugify('%s %s' % (self.nim, self.nama_lengkap.lower()))

        return super(Mahasiswa, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name_plural = 'Profil Mahasiswa'
        verbose_name_plural = 'Mahasiswa'


class Orangtua(models.Model):
    """Orangtua/Wali Mahasiswa"""
    mahasiswa       = models.ForeignKey('Mahasiswa', on_delete=models.CASCADE)
    nama_lengkap    = models.CharField(max_length=225)
    hubungan        = models.CharField(max_length=7, choices=HUBUNGAN, help_text='Keterangan hubungan keluarga')
    hubungan_lain   = models.CharField(null=True, blank=True, max_length=225, help_text='Opsional. Tuliskan hubungan apabila memilih hubungan lainnya')
    hp              = PhoneNumberField(help_text='Nomor hp aktif', null=True, blank=True)
    pekerjaan       = models.CharField(max_length=225, help_text='e.g Wiraswasta, dan lain-lain.', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.nama_lengkap   = self.nama_lengkap.title()
        if self.hubungan_lain: self.hubungan_lain  = self.hubungan_lain.title()
        self.pekerjaan      = self.pekerjaan.title() if self.pekerjaan else self.pekerjaan

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nama_lengkap
    
    class Meta:
        verbose_name_plural = 'Orang Tua/Wali'


class Dosen(models.Model):
    akun            = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='akun_dosen')
    program_studi   = models.ForeignKey('akademik.ProgramStudi', null=True, on_delete=models.SET_NULL, related_name='program_studi_dosen')
    nidn            = models.CharField('NIDN', max_length=20, primary_key=True)
    nama_lengkap    = models.CharField(max_length=150)
    jenis_kelamin   = models.CharField(max_length=1, choices=JENIS_KELAMIN)
    tempat_lahir    = models.CharField(max_length=40, null=True, blank=True)
    tanggal_lahir   = models.DateField(null=True, blank=True)
    agama           = models.CharField(max_length=9, choices=AGAMA, default='islam')
    kewarganegaraan = models.CharField(max_length=3, choices=[('WNI', 'WNI'), ('WNA', 'WNA')], default='WNI')
    alamat          = models.TextField(help_text='nama jalan, nomor rumah', null=True, blank=True)
    rt              = models.PositiveSmallIntegerField(help_text='rukun tetangga', verbose_name='RT', null=True, blank=True)
    rw              = models.PositiveSmallIntegerField(help_text='rukun warga', verbose_name='RW', null=True, blank=True)
    kelurahan       = models.CharField(max_length=30, verbose_name='Kelurahan / Desa', null=True, blank=True)
    kecamatan       = models.CharField(max_length=30, null=True, blank=True)
    kab_kota        = models.CharField(max_length=30, verbose_name='Kabupaten / Kota', null=True, blank=True)
    provinsi        = models.CharField(max_length=30, null=True, blank=True)
    kode_pos        = models.PositiveSmallIntegerField(null=True, blank=True)
    perguruan_tinggi= models.CharField(max_length=50)
    gelar_akademik  = models.CharField(max_length=30, null=True, blank=True)
    tahun_ijazah    = models.PositiveSmallIntegerField('Tanggal Ijazah', help_text='Format tahun', choices=YEAR_CHOICES())
    jenjang         = models.CharField(max_length=2, choices=[('S3', 'S3'), ('S2', 'S2'), ('S1', 'S1')])
    file_foto       = models.ImageField(upload_to='dosen/foto/', blank=True)
    status          = models.CharField(max_length=6, choices=[('Aktif', 'Aktif'), ('Keluar', 'Keluar')], default='Aktif')
    email           = models.EmailField('Alamat email', null=True, blank=True)
    nomor_handphone = PhoneNumberField('No. Handphone', null=True, blank=True)
    tanggal_masuk   = models.DateField(default=timezone.now)
    slug            = models.SlugField(blank=True, editable=False)
    dibuat_pada     = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.tempat_lahir   = checkNone(self.tempat_lahir)
        self.kelurahan      = checkNone(self.kelurahan)
        self.kecamatan      = checkNone(self.kecamatan)
        self.kab_kota       = checkNone(self.kab_kota)
        self.email          = self.akun.email if self.akun else None
        self.nomor_handphone= self.akun.phone_number if self.akun else None
        self.slug           = slugify('{}'.format(self.nama_lengkap.lower()))

        return super(Dosen, self).save(*args, **kwargs)
    
    def __str__(self):
        return '{} - {}'.format(self.nidn, self.nama_lengkap)
    
    class Meta:
        ordering = ('nidn',)
        verbose_name_plural = 'Dosen'



# Transaksi MHS
class TransaksiMahasiswa(models.Model):
    mahasiswa = models.ForeignKey('Mahasiswa', on_delete=models.CASCADE)
    transksi = models.CharField(max_length=8, choices=[('Aktif', 'Aktif'), ('Nonaktif', 'Nonaktif'), ('Cuti', 'Cuti'), ('DO', 'Drop-Out'), ('Lulus', 'Lulus'), ('Keluar', 'Keluar')])
    priode_awal = models.DateField()
    priode_akhir = models.DateField()
    keterangan = models.TextField(null=True, blank=True)
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)
    dibuat_oleh = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        null=True, blank=True, 
        editable=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    diperbarui_oleh = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        null=True, blank=True, 
        editable=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return 'Transaksi {}'.format(
            self.mahasiswa.nama_lengkap
        )


# Transaksi DSN
class TransaksiDosen(models.Model):
    dosen = models.ForeignKey('Dosen', on_delete=models.CASCADE)
    transksi = models.CharField(
        max_length=8, 
        choices=[
            ('Cuti', 'Cuti'), 
            ('Aktif', 'Aktif Mengajar'), 
            ('Cuti', 'Cuti'), 
            ('Studi', 'Studi Lanjut'), 
            ('Tugas', 'Tugas di Instansi Lain'), 
            ('Almarhum', 'Almarhum')]
    )
    priode_awal = models.DateField()
    priode_akhir = models.DateField()
    keterangan = models.TextField(null=True, blank=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)
    dibuat_oleh = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        null=True, blank=True, 
        editable=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    diperbarui_oleh = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        null=True, blank=True, 
        editable=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return 'Transaksi {}'.format(
            self.dosen.nama_lengkap
        )


class ProfilPerguruanTinggi(models.Model):
    status = models.BooleanField('Status PT', default=True)
    nama = models.CharField('Perguruan Tinggi' ,max_length=100, default='Akademi Keperawatan Keris Husada')
    tanggal_berdiri = models.DateField('Tanggal Berdiri', default=date(2001, 9, 28))
    no_sk = models.CharField('Nomor SK PT', max_length=12, default='409DT2008')
    tanggal_sk = models.DateField('Tanggal SK PT', default=date(2008, 1, 21))
    alamat = models.TextField(default='Jalan Yos Sudarso Komplek Marinir Cilandak')
    kab_kota = models.CharField('Kota/Kabupaten', max_length=100, default='Kota Jakarta Selatan')
    provinsi = models.CharField(max_length=50, default='D.K.I Jakarta')
    pos = models.PositiveIntegerField('Kode Post', default=12560)
    telepon = PhoneNumberField(default='+02178845502')
    fax = PhoneNumberField(default='+02178845502')
    email = models.EmailField(default='infor@akaperkerishusada.ac.id')
    website = models.CharField(max_length=30, default='www.akperkerishusada.ac.id')
