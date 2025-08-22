from django.db import models

# Create your models here.
class Students(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    j_date = models.DateField(default= "2004-10-09")
    phone_no = models.CharField(max_length=15)
    total_fees = models.IntegerField(default= 10000)
    # paid_fees = models.IntegerField(default= 5000)
    
    def __str__(self):
        return self.name
    
    @property
    def paid_fees(self):
        # Calculate from fee history
        return sum(fee.amount for fee in self.feehistory_set.filter(status='success'))
    
    @property
    def pending_fees(self):
        return self.total_fees-self.paid_fees
    
    @property
    def is_authenticated(self):
        return True