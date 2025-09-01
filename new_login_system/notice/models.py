from django.db import models

# Create your models here.
class Notices(models.Model):
    CATEGORY_CHOICES = [
        ('general',  'General'),
        ('academic', 'Academic'),
        ('exam',     'Exam'),
        ('event',    'Event'),
        ('urgent',   'Urgent'),
    ]
    PRIORITY_CHOICES = [
        ('normal',    'Normal'),
        ('important', 'Important'),
        ('urgent',    'Urgent'),
    ]
    STATUS_CHOICES = [
        ('published', 'Published'),
        ('draft',     'Draft'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    priority    = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateField(auto_now_add=False)
    
    def __str__(self):
        return self.title