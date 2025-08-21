from django.db import models

# Create your models here.
class Admins(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    img1 = models.ImageField(upload_to='qrcode_images/', blank=True, null=True)    


    def __str__(self):
        return self.name
class Notices(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Homework(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField()
    # image = models.ImageField(upload_to='homework_images/', blank=True, null=True)
    img1 = models.ImageField(upload_to='homework_images/', blank=True, null=True)    

    def __str__(self):
        return self.title
    

