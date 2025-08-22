from django.db import models

# Create your models here.
class Notices(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=False)

    def __str__(self):
        return self.title