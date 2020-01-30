from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


import datetime

def YEAR_CHOICES():
    return [(y,y) for y in range(2016, datetime.date.today().year + 20)]

def CURRENT_YEAR():
    return datetime.date.today().year

HARI = (
    (1, 'Senin'),
    (2, 'Selasa'),
    (3, 'Rabu'),
    (4, 'Kamis'),
    (5, "Jum'at"),
    (6, 'Sabtu'),
)

PARITAS = [
    ('ganjil', 'Ganjil'), ('genap', 'Genap')
]

SEMESTER = [
    (1, '1 (Satu)'), 
    (2, '2 (Dua)'), 
    (3, '3 (Tiga)'), 
    (4, '4 (Empat)'), 
    (5, '5 (Lima)'), 
    (6, '6 (Enam)'), 
    (7, '7 (Tujuh)'), 
    (8, '8 (Delapan)')
]


# Program Studi / Prodi
class ProgramStudi(models.Model):
    jenjang         = models.CharField('Kode Jenjang Pendidikan', max_length=10, default='D3')
    nama            = models.CharField('Program Studi', max_length=100)
    nama_jurusan    = models.CharField(max_length=100, null=True, blank=True, default='D3 Keperawatan')
    singkat         = models.CharField(max_length=3, help_text='Singkatan nama program studi')
    akreditasi      = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')])
    ketua           = models.CharField('Ketua Program Studi', max_length=100)
    tanggal_berdiri = models.DateField(default=datetime.date(2001, 9, 28))
    sk_penyelengaraan = models.CharField(max_length=20, default='15037/D/T/K-III/2013')
    tanggal_sk      = models.DateField(default=datetime.date(2013, 7, 3))
    dibuat_pada     = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.nama           = self.nama.title()
        self.singkat        = self.singkat.upper()
        self.ketua          = self.ketua.title()
        self.akreditasi     = self.akreditasi.upper()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nama_jurusan
    
    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Program Studi'


def default_paritas(args):
    if args % 2:
        return 'ganjil'
    else:
        return 'genap'

# Matakuliah
class Matakuliah(models.Model):
    kode            = models.CharField(max_length=13, primary_key=True)
    nama            = models.CharField('Nama matakuliah (ind)', max_length=100, help_text='Nama mata kuliah dalam bahasa Indonesia')
    nama_asing      = models.CharField('Nama matakuliah (Eng)', max_length=100, null=True, blank=True, help_text='Nama mata kuliah dalam bahasa Inggris')
    sks             = models.PositiveSmallIntegerField(_('SKS'))
    semester        = models.PositiveSmallIntegerField(choices=SEMESTER)
    aktif           = models.BooleanField(_('status aktif'),default=True)
    program_studi   = models.ForeignKey('ProgramStudi', on_delete=models.CASCADE)
    dibuat_pada     = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.nama   = self.nama.title()
        return super(Matakuliah, self).save(*args, **kwargs)

    def __str__(self):
        return '{} - {} - {} SKS - smt {}'.format(
            self.kode, 
            self.nama, 
            self.sks, 
            self.get_semester_display(), 
        )
    
    class Meta:
        ordering = ('kode',)
        verbose_name_plural = 'Matakuliah'


# Ruang Kuliah
class RuangKuliah(models.Model):
    kode            = models.CharField(max_length=10, primary_key=True)
    nama_ruangan    = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.nama_ruangan = self.nama_ruangan.title()
        return super(RuangKuliah, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.kode
    
    class Meta:
        verbose_name_plural = 'Ruang Kuliah'


# Jadwal
class Jadwal(models.Model):
    matakuliah      = models.OneToOneField('Matakuliah', null=True, on_delete=models.CASCADE)
    dosen           = models.ManyToManyField('manajemen.Dosen')
    hari            = models.PositiveSmallIntegerField(choices=HARI)
    jam_mulai       = models.TimeField()
    jam_akhir       = models.TimeField()
    tampil          = models.BooleanField(default=True)
    ruang_kuliah    = models.ForeignKey('RuangKuliah', null=True, on_delete=models.SET_NULL)
    dibuat_pada     = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Semester: %s |Hari: %s |Matakuliah: %s |SKS: %s |Waktu: %s - %s |Dosen: %s |Ruang: %s |Prodi: %s' % (
            self.matakuliah.get_semester_display() if self.matakuliah else '',
            self.get_hari_display(), 
            self.matakuliah.nama if self.matakuliah else None, 
            self.matakuliah.sks if self.matakuliah else None,
            self.jam_mulai, 
            self.jam_akhir, 
            ' / '.join([i.nama_lengkap for i in self.dosen.all()]),
            self.ruang_kuliah,
            self.matakuliah.program_studi.singkat if self.matakuliah else None
        )
    
    class Meta:
        ordering = (
            'matakuliah__semester',
            'hari',
            'jam_mulai',
        )
        verbose_name_plural = 'Jadwal'


# KRS
class Krs(models.Model):
    jadwal              = models.ForeignKey('Jadwal', verbose_name='Jadwal Matakuliah', on_delete=models.CASCADE, null=True, blank=True)
    mahasiswa           = models.ForeignKey('manajemen.Mahasiswa', on_delete=models.CASCADE)
    acc_dosen           = models.BooleanField(default=True)
    status              = models.CharField(max_length=8, choices=[
                        ('Baru', 'Baru'), ('Remedial', 'Remedial')
                        ], default='Baru')
    dibuat_pada         = models.DateTimeField(auto_now_add=True)
    diperbarui_pada     = models.DateTimeField(auto_now=True)


    def __str__(self):
        return ('Mahasiswa: {} - {} | Matakuliah: {} | Dosen: {} | Status ambil: {}'.format(
        self.mahasiswa.nim,
        self.mahasiswa.nama_lengkap,
        self.jadwal.matakuliah.nama if self.jadwal.matakuliah.nama else '-none',
        '/'.join([dosen.nama_lengkap for dosen in self.jadwal.dosen.all()]),
        self.status,
    ))

    class Meta:
        ordering            = ('id',)
        verbose_name_plural = 'KRS'


# Absensi Mahasiswa
class Absensi(models.Model):
    jadwal = models.ForeignKey('Jadwal', on_delete=models.CASCADE)
    mahasiswa = models.ForeignKey('manajemen.Mahasiswa', on_delete=models.CASCADE)
    paraf = models.CharField(max_length=5, choices=[('Hadir', 'Hadir'), ('Alfa', 'Alfa'), ('Izin', 'Izin'), ('Sakit', 'Sakit')], default='Hadir')
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
        return 'Mahasiswa {}  Jadwal'.format(self.jadwal.id, self.mahasiswa.nama_lengkap)
    
    class Meta:
        verbose_name_plural = 'Absensi mahasiswa'


# Nilai Semester
class NilaiSemester(models.Model):
    krs             = models.OneToOneField(
        'Krs',
        null=True,
        on_delete=models.CASCADE
    )
    mahasiswa       = models.ForeignKey('manajemen.Mahasiswa', on_delete=models.CASCADE)
    matakuliah      = models.ForeignKey('Matakuliah', on_delete=models.CASCADE)
    absensi         = models.PositiveIntegerField(null=True, blank=True)
    tugas           = models.FloatField(null=True, blank=True)
    uts             = models.FloatField(null=True, blank=True)
    uas             = models.FloatField(null=True, blank=True)
    total           = models.FloatField(
        choices=[
            (4, 'A'), (3.5, 'B+'), (3, 'B'), 
            (2.5, 'C+'), (2, 'C'), (1, 'D'), (0, 'E')
        ],
        null=True, blank=True
    )

    def __str__(self):
        return 'Tugas: {} | UTS: {} | UAS: {}'.format(
            self.tugas,
            self.uts,
            self.uas,
        )
    dinilai_pada     = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Nilai'





















# def TAHUN_AJARAN_SMT():
#     return [(str(a), (
#                 (a, '{} Genap'.format(a)),
#                 (a + 0.5, '{} Ganjil'.format(a))
#             )) for a in range(2016, datetime.date.today().year + 30)]
# # kelas
# class Kelas(models.Model):
#     jadwal = models.ForeignKey('Jadwal', on_delete=models.CASCADE)
#     nama_kelas = models.CharField(max_length=50, help_text='Nama kelas matakuliah. eg. Kelas Agama')
#     tahun_ajaran_semester = models.PositiveIntegerField(
#         choices=TAHUN_AJARAN_SMT()
#     )
#     kelas_mahasiswa = models.ManyToManyField('mahasiswa.Profile', through='KelasMahasiswa')


# # Kelas Mahasiswa
# class KelasMahasiswa(models.Model):
#     kelas = models.ForeignKey('Kelas', on_delete=models.CASCADE)
#     mahasiswa = models.ForeignKey('mahasiswa.Profile', null=True, on_delete=models.SET_NULL)


# KHS / Kartu Hasil Studi
# class KHS(models.Model):
#     krs = models.OneToOneField(
#         'KRS',
#         on_delete=models.CASCADE,
#         help_text='tidak bisa pilih bila status ambil telah ada'
#     )
#     status = models.CharField(
#         max_length=5, 
#         choices=[
#             ('Lulus', 'Lulus'),
#             ('Gagal', 'Gagal'),
#             ('Aktif', 'Aktif')
#         ],
#         default='Aktif',
#     )
#     dibuat_pada     = models.DateTimeField(auto_now_add=True)
#     diperbarui_pada = models.DateTimeField(auto_now=True)
#     dibuat_oleh     = models.ForeignKey(
#         'core.User', 
#         null=True, blank=True, 
#         editable=False,
#         on_delete=models.SET_NULL,
#         related_name='dibuatnya_khs_oleh_user'
#     )
#     diperbarui_oleh = models.ForeignKey(
#         'core.User', 
#         null=True, blank=True, 
#         editable=False,
#         on_delete=models.SET_NULL,
#         related_name='diperbaruinya_khs_oleh_user'
#     )

#     def __str__(self):
#         return '{} | Matakuliah: {}'.format(
#             self.krs.mahasiswa.nama_lengkap,
#             self.krs.jadwal.matakuliah.nama,
#         )
    
#     class Meta:
#         verbose_name_plural = 'KHS'

