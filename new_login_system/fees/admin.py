# Register your models here.
# In fees/admin.py
from django.contrib import admin
from django.utils import timezone
from .models import FeeHistory

@admin.register(FeeHistory)
class FeeHistoryAdmin(admin.ModelAdmin):
    # list_display = ['student_id', 'amount', 'status', 'method', 'payment_date', 'reviewed_by']
    # list_filter = ['status', 'method', 'payment_date']
    # search_fields = ['student_id__name', 'student_id__email']
    # readonly_fields = ['payment_date', 'student_id', 'amount', 'method', 'img1', 'remarks']
    
    # fieldsets = (
    #     ('Payment Details', {
    #         'fields': ('student_id', 'amount', 'method', 'payment_date', 'remarks', 'img1')
    #     }),
    #     ('Admin Review', {
    #         'fields': ('status', 'failure_reason', 'admin_remarks', 'reviewed_by', 'reviewed_date')
    #     }),
    # )
    
    def save_model(self, request, obj, form, change):
        if change and obj.status in ['success', 'failed']:
            if not obj.reviewed_date:
                obj.reviewed_date = timezone.now()
        super().save_model(request, obj, form, change)
