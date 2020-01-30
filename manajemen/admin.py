from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import *


# django import export
from import_export.admin import ImportExportModelAdmin
from import_export.tmp_storages import CacheStorage
from .resources import *

class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'username', 'email', 'phone_number',
        'user_type', 'is_staff', 'is_active',
        'avatar', 'date_joined', 
    )

    list_filter = (
        'user_type', 'date_joined',
    )

    search_fields = (
        'username', 'email'
    )

    fieldsets = (
        (None, {
            'fields': (
                'username', 'password', 'email',
                'phone_number', 'avatar'
            )
        }),
        (_('Permissions'), {
            'fields': (
                ('user_type', 'is_active'),
                'is_staff', 'is_superuser', 'user_permissions',
                'groups'
            )
        }),
        (_('Important dates'), {
            'fields': (
                'last_login', 'date_joined'
            )
        })
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'user_type', 'password1', 'password2')}
        ),
    )

    filter_horizontal = ()

    readonly_fields = (
        'date_joined',
    )

admin.site.register(User, CustomUserAdmin)


@admin.register(Angkatan)
class AngkatanAdmin(admin.ModelAdmin):
    fields = (
        'tahun',
        'semester',
    )

    list_display = (
        'tahun',
        'semester',
    )


class TransaksiMahasiswaInline(admin.StackedInline):
    model = TransaksiMahasiswa
    extra = 0

@admin.register(Mahasiswa)
class MahasiswaAdmin(ImportExportModelAdmin):
    resource_class = MahasiswaResource
    tmp_storage_class = CacheStorage

    inlines = (
        TransaksiMahasiswaInline,
    )
    
    fieldsets = (
        (None, {
            'fields': (
                'nama_lengkap',
                ('tempat_lahir', 'tanggal_lahir'),
                'ktp',
                ('jenis_kelamin', 'agama'),
                ('gol_darah', 'kewarganegaraan'),
            ),
        }),
        ('Alamat Rumah', {
            'fields': (
                ('alamat','rt', 'rw'),
                ('kelurahan', 'kecamatan'),
                ('kab_kota', 'provinsi', 'kode_pos')
            )
        }),
        ('Kontak', {
            'fields': (
                'nomor_telepon',
                'nomor_handphone',
                'email',
            )
        }),
        ('Akademik', {
            'fields': (
                'akun',
                'program_studi',
                'file_foto',
                'nim',
                'status',
                'status_awal',
                'angkatan',
                'tahun_semester_masuk',
                'tanggal_masuk',
            )
        }),
    )

    list_display = (
        # 'program_studi',
        'nim',
        'nama_lengkap',
        'jenis_kelamin',
        'status',
        'akun',
    )

    list_display_links = (
        'nim',
        'nama_lengkap',
    )

    list_filter = (
        'akun',
        # 'program_studi',
        'provinsi',
        'kab_kota',
    )

    readonly_fields = (
        'slug',
        'dibuat_pada',
        'diperbarui_pada',
    )

    search_fields = (
        'nim',
        'nama_lengkap',
    )

    def Nama_mahasiswa(self, obj):
        return obj.nama_lengkap

    def alamat_lengkap(self, obj):
        return "{}, RT.{} RW.{}, {}, {}, {}, {}, {}".format(
            is_empty(obj.alamat), 
            is_empty(obj.rt),
            is_empty(obj.rw), 
            is_empty(obj.kelurahan), 
            is_empty(obj.kecamatan), 
            is_empty(obj.kab_kota), 
            is_empty(obj.provinsi),
            is_empty(obj.kode_pos)
        )
    alamat_lengkap.empty_value_display = 'belum ada nilai'


@admin.register(Orangtua)
class OrangtuaAdmin(admin.ModelAdmin):
    empty_value_display = 'belum ada nilai'

    fieldsets = (
        (None, {
            'fields': (
                'mahasiswa',
                'nama_lengkap',
                ('hubungan', 'hubungan_lain'),
                ('hp','pekerjaan'),
            )
        }),
    )

    list_display = (
        'id',
        'nama_lengkap',
        'hp',
        'orangtua_dari',
        'hubungan',
        'pekerjaan'
    )

    list_display_links = (
        'nama_lengkap',
    )

    list_filter = (
        'hubungan',
        'mahasiswa',
    )

    search_fields = (
        'nama_lengkap',
        'mahasiswa',
    )

    def orangtua_dari(self, obj):
        mhs = []
        for i in obj.profile.all():
            mhs.append(f'{i.nim} {i.namal_engkap}')
        return mark_safe('<br/>'.join(mhs))


class TransaksiDosenInline(admin.StackedInline):
    model = TransaksiDosen
    extra = 0

@admin.register(Dosen)
class DosenAdmin(ImportExportModelAdmin):
    empty_value_display = '-'
    # import export
    resource_class = DosenResource
    tmp_storage_class = CacheStorage

    inlines = (
        TransaksiDosenInline,
    )

    fieldsets = (
        (None, {
            'fields': (
                'program_studi', 
                'nidn',
                'nama_lengkap',
                'jenis_kelamin',
                'tempat_lahir', 
                'tanggal_lahir',
                'agama', 
                'kewarganegaraan',
                'status',
                ('akun', 'file_foto'),
            ),
        }),
        ('Alamat Tempat Tinggal', {
            'fields': (
                'alamat',
                ('rt', 'rw'),
                ('kelurahan', 'kecamatan'),
                ('kab_kota', 'provinsi', 'kode_pos')
            )
        }),
        ('Riwayat Pendidikan', {
            'fields': (
                'perguruan_tinggi',
                'gelar_akademik',
                'tahun_ijazah',
                'jenjang',
            )
        }),
        ('Kotak', {
            'fields': (
                'email',
                'nomor_handphone',
            )
        }),
        ('Tanggal Penting', {
            'fields': (
                'tanggal_masuk',
                'dibuat_pada',
                'diperbarui_pada'
            )
        })
    )

    readonly_fields = (
        'dibuat_pada', 'diperbarui_pada'
    )

    list_display = (
        'nidn',
        'akun',
        'nama_lengkap',
        'jenis_kelamin',
        'Tempat_tanggal_lahir',
        'pendidikan',
        'status',
        'alamat',
        'kab_kota',
        'provinsi',
        'tanggal_masuk',
    )

    list_display_links = (
        'nidn', 
        'nama_lengkap'
    )

    def pendidikan(self, obj):
        return obj.jenjang

    def Tempat_tanggal_lahir(self, obj):
        return '{}, {}'.format(
            obj.tempat_lahir,
            obj.tanggal_lahir
        )
