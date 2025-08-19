from django.db import models

# Create your models here.
class Students(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    j_date = models.DateField(default= "2004-10-09")
    phone_no = models.IntegerField(default= 1234567890)
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
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=255, blank=True)
    img1 = models.CharField(max_length=500, blank=True, null=True)
    def __str__(self):
        return f"{self.student_id.name} - {self.amount}"
    
    class Meta:
        verbose_name_plural = "Fee Histories"
