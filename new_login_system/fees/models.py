from django.db import models
from students.models import Students

# Create your models here.
class FeeHistory(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('fail', 'Fail'),
    )
    METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('online', 'Online'),
    )
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=255, blank=True)
    img1 = models.ImageField(upload_to='feehistory_images/', blank=True, null=True)    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='cash')
    
    def __str__(self):
        return f"{self.student_id.name} - {self.amount}"
    
    class Meta:
        verbose_name_plural = "Fee Histories"
