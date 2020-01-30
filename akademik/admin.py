from django.contrib import admin
from .models import *

# django import export
from import_export.admin import ImportExportModelAdmin
from import_export.tmp_storages import CacheStorage
from .resources import MatakuliahResource, JadwalResource

# Program studi / prodi Admin
@admin.register(ProgramStudi)
class ProgramStudiAdmin(admin.ModelAdmin):
    empty_value_display = 'belum ada nilai'
    
    fieldsets = (
        (None, {
            'fields': (
                'jenjang',
                'nama', 
                'nama_jurusan',
                'singkat',
                'akreditasi',
                'ketua',
            )
        }),
        ('Kredensial', {
            'fields': (
                'tanggal_berdiri',
                'sk_penyelengaraan',
                'tanggal_sk',
            )
        })
    )

    list_display = (
        'id', 'nama', 'singkat',
        'ketua', 'akreditasi', 
        'dibuat_pada', 'diperbarui_pada',
    )

    list_display_links = (
        'nama', 'singkat',
    )

    list_filter = (
        'akreditasi', 'ketua',
    )

    search_fields = (
        'nama', 'singkat',
    )


# Matakuliah Admin
@admin.register(Matakuliah)
class MatakuliahAdmin(ImportExportModelAdmin):
    empty_value_display = 'belum ada nilai'

    # import export
    resource_class = MatakuliahResource
    tmp_storage_class = CacheStorage
    
    fieldsets = (
        (None, {
            'fields': (
                'kode',
                ('nama', 'nama_asing'), 
                'sks', 
                'aktif',
                ('semester', 'program_studi'),
            )
        }),
    )

    list_display = (
        'kode',
        'nama', 
        'sks', 
        'Semester',
        'aktif',
        'Program_studi',
        'dibuat_pada', 
        'diperbarui_pada',
    )

    list_display_links = (
        'kode', 'nama',
    )

    list_filter = (
        'sks', 'program_studi', 'aktif',
    )

    search_fields = (
        'kode', 'nama',
    )

    def Semester(self, obj):
        return '{}'.format(
            obj.semester,
        )
    
    def Program_studi(self, obj):
        return obj.program_studi.singkat


# Ruang Kuliah Admin
@admin.register(RuangKuliah)
class RuangKuliahAdmin(admin.ModelAdmin):
    empty_value_display = 'belum ada nilai'

    fieldsets = (
        (None, {
            'fields': (
                ('kode', 'nama_ruangan'),
            )
        }),
    )

    list_display = (
       'kode', 'nama_ruangan',
    )

    list_display_links = (
        'kode', 'nama_ruangan',
    )

    search_fields = (
        'kode', 'nama_ruangan',
    )


class AbsensiInline(admin.StackedInline):
    model = Absensi
    extra = 0

# Jadwal Admin
@admin.register(Jadwal)
class JadwalAdmin(ImportExportModelAdmin):
    resource_class = JadwalResource
    tmp_storage_class = CacheStorage
    empty_value_display = 'belum ada nilai'
    
    inlines = (
        AbsensiInline,
    )

    fieldsets = (
        (None, {
            'fields': (
                'matakuliah', 
                'dosen',
                'tampil',
            ),
        }),
        ('Hari, Waktu & Tempat', {
            'fields': (
                ('hari', 'ruang_kuliah'),
                ('jam_mulai', 'jam_akhir')
            )
        })
    )

    list_display = (
        'id',
        'Semester',
        'hari',
        'kode',
        'Matakuliah',
        'sks',
        'Dosen',
        'waktu',
        'ruang',
        'prodi',
        'Mahasiswa',
    )

    list_display_links = (
        'id', 'Matakuliah',
    )

    list_filter = (
        'matakuliah__kode',
        'dosen__nidn',
        'krs__mahasiswa__nama_lengkap',
        'hari',
    )

    def kode(self,obj):
        return obj.matakuliah.kode if obj.matakuliah else '?'

    def Matakuliah(self, obj):
        return obj.matakuliah.nama if obj.matakuliah else '?'
    
    def sks(self, obj):
        return obj.matakuliah.sks if obj.matakuliah else '?'

    def Semester(self, obj):
        return '{}'.format(
            obj.matakuliah.semester if obj.matakuliah else '?',
        )
    
    def Dosen(self, obj):
        return ' / '.join([i.nama_lengkap for i in obj.dosen.all()])

    def waktu(self, obj):
        return '%s - %s' % (obj.jam_mulai, obj.jam_akhir)
    
    def ruang(self, obj):
        return obj.ruang_kuliah
    
    def prodi(self, obj):
        return obj.matakuliah.program_studi if obj.matakuliah else '?'

    def Mahasiswa(self, obj):
        return '{} Mahasiswa'.format(obj.krs_set.count() if obj.krs_set.exists() else 0)


# KRS
@admin.register(Krs)
class KrsAdmin(admin.ModelAdmin):
    empty_value_display = 'belum ada nilai'
    fieldsets = (
        (None, {
            'fields': (
                'mahasiswa',
                ('jadwal',),
                ('acc_dosen', 'status'),
            )
        }),
    )

    list_display = (
        'Nim',
        'Mahasiswa', 
        'Matakuliah', 
        'Semester',
        # 'Hari',
        # 'Sks',
        # 'Waktu',
        # 'Dosen',  
        # 'Ruang',
        # 'Prodi',
    )

    def Nim(self, obj):
        return obj.mahasiswa.nim

    def Mahasiswa(self, obj):
        return obj.mahasiswa.nama_lengkap
    
    def Matakuliah(self, obj):
        return obj.jadwal.matakuliah.nama
    
    def Semester(self, obj):
        return obj.jadwal.matakuliah.get_semester_display()

    # def Hari(self, obj):
    #     return format_html_join(
    #         '\n', "<li>{}</li>",
    #         ((
    #             jadwal.get_hari_display(),
    #         ) for jadwal in obj.jadwal_matakuliah.all())
    #     )
    
    # def Sks(self, obj):
    #     return format_html_join(
    #         '\n', "<li>{}</li>",
    #         ((
    #             jadwal.matakuliah.sks if jadwal.matakuliah else '?',
    #         ) for jadwal in obj.jadwal_matakuliah.all())
    #     )
    
    # def Waktu(self, obj):
    #     return format_html_join(
    #         '\n', "<li>{} - {}</li>",
    #         ((
    #             jadwal.jam_mulai,
    #             jadwal.jam_akhir,
    #         ) for jadwal in obj.jadwal_matakuliah.all())
    #     )
    
    # def Dosen(self, obj):
    #     return format_html_join(
    #         '\n', "<li>{}</li>", ((
    #             '/'.join([d.nama_lengkap for d in jadwal.dosen.all()]),
    #         ) for jadwal in obj.jadwal_matakuliah.all())
    #     )

    # def Ruang(self, obj):
    #     return format_html_join(
    #         '\n', "<li>{}</li>", ((
    #             jadwal.ruang_kuliah.kode,
    #         ) for jadwal in obj.jadwal_matakuliah.all())
    #     )
    
    # def Prodi(self, obj):
    #     return format_html_join(
    #         '\n', "<li>{}</li>", ((
    #             jadwal.matakuliah.program_studi.singkat
    #             if jadwal.matakuliah else '?',
    #         ) for jadwal in obj.jadwal_matakuliah.all())
    #     )

    # search_fields = (
    #     'mahasiswa__nim',
    #     'mahasiswa__nama_lengkap',
    #     'jadwal_matakuliah__matakuliah__nama',
    #     'jadwal_matakuliah__dosen__nama_lengkap',
    # )

    # list_display_links = (
    #     'Nim',
    #     'Mahasiswa',
    #     'Matakuliah',
    # )

    # list_filter = (
    #     'jadwal_matakuliah__matakuliah__program_studi',
    #     'jadwal_matakuliah__ruang_kuliah',
    #     'jadwal_matakuliah__jam_mulai',
    #     'jadwal_matakuliah__matakuliah__semester',
    #     'jadwal_matakuliah__matakuliah__sks',
    #     'jadwal_matakuliah__hari',
    #     'status',
    # )



# Nilai Semester
@admin.register(NilaiSemester)
class NilaiSemesterAdmin(admin.ModelAdmin):

    fields = (
        'krs',
        'mahasiswa',
        'matakuliah',
        'absensi',
        'tugas',
        'uts',
        'uas',
        'total'
    )

    list_display = (
        'krs',
        'matakuliah',
        'absensi',
        'tugas',
        'uts',
        'uas',
        'total'
    )

    list_display_links = (
        'matakuliah',
    )