from django.db import models
from students.models import Students
# Create your models here.
class Attendance(models.Model):
    student = models.ForeignKey(Students, related_name= "attendances", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    present = models.BooleanField(default = False)
    # created_at = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        unique_together = ('student','date')
        ordering = ['-date']
    
    def __str__(self):
        status = 'Present' if self.present else 'Absent'
        return f"{self.student.name} - {self.date}: {status}"
    