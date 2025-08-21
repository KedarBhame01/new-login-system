from django.db import models

# Create your models here.
class Homework(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField()
    # image = models.ImageField(upload_to='homework_images/', blank=True, null=True)
    img1 = models.ImageField(upload_to='homework_images/', blank=True, null=True)    

    def __str__(self):
        return self.title
    