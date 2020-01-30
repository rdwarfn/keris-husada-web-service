from import_export import resources, widgets
from import_export.fields import Field
from .models import *
from akademik.models import ProgramStudi

class MahasiswaResource(resources.ModelResource):
    akun = Field(column_name='akun', readonly=True)
    slug = Field(column_name='slug', readonly=True)
    angkatan = Field(column_name='angkatan', readonly=True)
    tahun_semester_masuk = Field(column_name='tahun_semester_masuk', readonly=True)
    dibuat_pada = Field(column_name='dibuat_pada', readonly=True)
    diperbarui_pada = Field(column_name='diperbarui_pada', readonly=True)
    class Meta:
        model = Mahasiswa


class DosenResource(resources.ModelResource):
    akun = Field(column_name='akun', readonly=True)
    file_foto = Field(column_name='file_foto', readonly=True)
    status = Field(column_name='status', readonly=True)
    tanggal_masuk = Field(column_name='tanggal_masuk', readonly=True)
    slug = Field(column_name='slug', readonly=True)
    dibuat_pada = Field(column_name='dibuat_pada', readonly=True)
    diperbarui_pada = Field(column_name='diperbarui_pada', readonly=True)
    # program_studi = Field(
    #     column_name='program_studi',
    #     widget=widgets.ForeignKeyWidget(
    #         ProgramStudi, 'id'
    #     )
    # )

    class Meta:
        model = Dosen
        import_id_fields = ('nidn',)
        skip_unchanged = True
        report_skipped = False
        fields = (
            'akun',
            'file_foto',
            'tanggal_masuk',
            'slug',
            'dibuat_pada',
            'diperbarui_pada',
            'program_studi',
            'nidn',
            'nama_lengkap',
            'jenis_kelamin',
            'templat_lahir',
            'tanggal_lahir',
            'agama',
            'kewarganegaraan',
            'alamat',
            'rt',
            'rw',
            'kelurahan',
            'kecamatan',
            'kab_kota',
            'provinsi',
            'kode_pos',
            'perguruan_tinggi',
            'gelar_akademik',
            'tahun_ijazah',
            'email',
            'nomor_handphone',
        )

