from django.db import models
from django.db.models import Sum, F, Value, Q
from django.db.models.functions import Coalesce


# Create your models here.
class StudentsManager(models.Manager):
    def with_fee_calculations(self):
        return self.annotate(
            paid_fees=Coalesce(
                Sum('feehistory__amount', filter=Q(feehistory__status='success')), 
                Value(0)
            ),
            pending_fees=F('total_fees') - F('paid_fees')
        )

class Students(models.Model):
    objects = StudentsManager()
    ACCOUNT_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive') ,
    )
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    j_date = models.DateField(default= "2004-10-09")
    phone_no = models.CharField(max_length=15)
    total_fees = models.IntegerField(default= 10000)
    account = models.CharField(max_length=10, choices=ACCOUNT_CHOICES, default='inactive')

    def __str__(self):
        return self.name
    
    # @property
    # def paid_fees(self):
    #     # Calculate from fee history
    #     return sum(fee.amount for fee in self.feehistory_set.filter(status='success'))
    
    # @property
    # def pending_fees(self):
    #     return self.total_fees-self.paid_fees
    
    # @property
    # def is_authenticated(self):
    #     return True