from django.contrib import admin
from django.utils.text import Truncator
from django_summernote.admin import SummernoteModelAdmin, SummernoteInlineModelAdmin
from .models import *

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):

    fields = (
        'nama',
    )


class SubArtikel(admin.StackedInline): #SummernoteInlineModelAdmin
    model = SubArtikel
    extra = 0

@admin.register(Artikel)
class ArtikelAdmin(admin.ModelAdmin): # SummernoteModelAdmin
    inlines = (SubArtikel,)

    fields = (
        'kategori',
        'foto',
        'judul',
        'isi',
    )

    list_display = (
        'kategori',
        'foto',
        'judul',
        'Truncate',
        'dibuat_pada',
        'diperbarui_pada',
        'dibuat_oleh'
    )

    def Truncate(self, obj):
        return Truncator(obj.isi).words(10)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # set dibuat_oleh hanya pada saat pertama kali
            obj.dibuat_oleh = request.user
        obj.diperbarui_oleh = request.user
        super().save_model(request, obj, form, change)
