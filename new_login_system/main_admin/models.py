from django.db import models

# Create your models here.
class Admins(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

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
    image = models.ImageField(upload_to='homework_images/', blank=True, null=True)
    def __str__(self):
        return self.title
    
class Attendance(models.Model):
    student = models.ForeignKey("students.Students", related_name= "attendances", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    present = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        unique_together = ('student','date')
        ordering = ['-date']
    
    def __str__(self):
        status = 'Present' if self.present else 'Absent'
        return f"{self.student.name} - {self.date}: {status}"
    
class Calender(models.Model):
    date = models.DateField(unique=True)
    present = models.BooleanField(default=False)
    detail = models.TextField()

    def __str__(self):
        status = 'Yes' if self.present else 'No'
        return f"{self.date}:{status}:{self.detail}"