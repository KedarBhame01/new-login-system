from django.db import models

# Create your models here.
class Admins(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=100)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name
class Notices(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
