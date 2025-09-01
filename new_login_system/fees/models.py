from django.db import models

# Create your models here.
class FeeHistory(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )
    METHOD_CHOICES = (
        ('online', 'Online'),
        ('cash', 'Cash'),
    )
    student_id = models.ForeignKey("students.Students", on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_date = models.DateField(auto_now_add=True)
    payment_time = models.TimeField(auto_now_add=True)
    remarks = models.CharField(max_length=255, blank=True)
    img1 = models.ImageField(upload_to='feehistory_images/', blank=True, null=True)    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='cash')
    admin_remarks = models.TextField(blank=True, null=True, help_text="Admin's reason for approval/rejection")
    reviewed_date = models.DateTimeField(blank=True, null=True)
    failure_reason = models.CharField(
        max_length=50,
        choices=[
            ('insufficient_proof', 'Insufficient Payment Proof'),
            ('wrong_amount', 'Wrong Amount'),
            ('duplicate_payment', 'Duplicate Payment'),
            ('invalid_receipt', 'Invalid Receipt/Screenshot'),
            ('other', 'Other (see admin remarks)')
        ],
        blank=True,
        null=True
    )
    def __str__(self):
        return f"{self.student_id.name} - {self.amount}"
    
    class Meta:
        verbose_name_plural = "Fee Histories"
