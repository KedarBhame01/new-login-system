from django.db import models

# Create your models here.
class Calender(models.Model):
    date = models.DateField(unique=True)
    present = models.BooleanField(default=False)
    detail = models.TextField()

    def __str__(self):
        status = 'Yes' if self.present else 'No'
        return f"{self.date}:{status}:{self.detail}"