from import_export import resources, widgets
from import_export.fields import Field
from .models import Matakuliah, Jadwal
from manajemen.models import Dosen


class MatakuliahResource(resources.ModelResource):
    aktif = Field(column_name='aktif', readonly=True)
    dibuat_pada = Field(column_name='dibuat_pada', readonly=True)
    diperbarui_pada = Field(column_name='diperbarui_pada', readonly=True)

    class Meta:
        model = Matakuliah
        import_id_fields = ('kode',)


class JadwalResource(resources.ModelResource):
    # matakuliah = Field(column_name='matakuliah', readonly=True)
    # ruang_kuliah = Field(column_name='ruang_kuliah', readonly=True)
    # id = Field(column_name='id', readonly=True)
    # dosen = Field(
    #     column_name='dosen',
    #     widget=widgets.ForeignKeyWidget(Dosen, 'nidn')
    # )
    # matakuliah = Field(
    #     column_name='matakuliah',
    #     widget=widgets.ForeignKeyWidget(Matakuliah, 'kode')
    # )
    dibuat_pada = Field(column_name='dibuat_pada', readonly=True)
    diperbarui_pada = Field(column_name='diperbarui_pada', readonly=True)

    class Meta:
        model = Jadwal
        # fields = (
        #     'matakuliah',
        #     'id',
        #     'dosen',
        #     'hari',
        #     'jam_mulai',
        #     'jam_akhir',
        #     'tampil',
        #     'ruang_kuliah',
        # )
