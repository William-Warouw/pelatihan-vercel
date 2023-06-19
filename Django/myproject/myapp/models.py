from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Barang(models.Model):
    nama_barang = models.CharField(max_length=50)
    jenis_barang = models.CharField(max_length=50, null=True)
    jumlah = models.IntegerField()

    def __str__(self) -> str:
        return self.nama_barang
    
class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    release_date = models.DateField(null=True)


    def __str__(self):
        return self.title

class Track(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    duration = models.DurationField()
    

    def __str__(self):
        return self.title
