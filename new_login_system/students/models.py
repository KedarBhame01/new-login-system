from django.db import models

# Create your models here.
class Students(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    j_date = models.DateField(default= "2004-10-09")
    phone_no = models.CharField(max_length=15, default= 0000000000)
    total_fees = models.IntegerField(default= 10000)
    # paid_fees = models.IntegerField(default= 5000)
    
    def __str__(self):
        return self.name
    
    @property
    def paid_fees(self):
        # Calculate from fee history
        return sum(fee.amount for fee in self.feehistory_set.all())
    
    @property
    def pending_fees(self):
        return self.total_fees-self.paid_fees
    
    @property
    def is_authenticated(self):
        return True
class FeeHistory(models.Model):
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('fail', 'Fail'),
    )
    METHOD_CHOICES = (
        ('online', 'Online'),
        ('cash', 'Cash'),
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
