from django.db import models
from django.conf import settings

class Kategori(models.Model):
    nama = models.CharField(max_length=30)

    def __str__(self):
        return self.nama

# class Image(models.Model):
#     file = models.ImageField(upload_to='Subartikel/Image')


class Artikel(models.Model):
    kategori = models.ForeignKey('Kategori', null=True, on_delete=models.SET_NULL)
    foto = models.ImageField(null=True, blank=True, upload_to='Artikel/Image')
    judul = models.CharField(max_length=100)
    isi = models.TextField()
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)
    dibuat_oleh = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+'
    )

    def __str__(self):
        return self.judul

    def save(self, *args, **kwargs):
        self.judul = self.judul.title()
        return super().save(*args, **kwargs)



class SubArtikel(models.Model):
    artikel = models.ForeignKey('Artikel', on_delete=models.CASCADE)
    judul = models.CharField(max_length=100)
    isi = models.TextField()

    def __str__(self): 
        return self.judul
    
    def save(self, *args, **kwargs):
        self.judul = self.judul.title();
        return super().save(*args, **kwargs)