from django.db import models

# Create your models here.
class Admins(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    img1 = models.ImageField(upload_to='qrcode_images/', blank=True, null=True)    


    def __str__(self):
        return self.name