from django.shortcuts import render
from .serializers import FeeHistorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.viewsets import ModelViewSet
from .models import FeeHistory
from students.models import Students
# JWT authentication class

from utils.base_viewsets import BaseCRUDViewSet
from utils.base_viewsets import success_response, error_response

from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django.utils import timezone
# Create your views here.
def dashboard_view(request):
    return render(request, 'fees/dashboard.html')
class FeeHistoryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
class FeeHistoryAPI(BaseCRUDViewSet):
    queryset = FeeHistory.objects.all()
    serializer_class = FeeHistorySerializer
    pagination_class = FeeHistoryPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'method', 'student_id']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by student_id
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student_id=student_id)

        # Date range filtering
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(payment_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(payment_date__lte=end_date)

        return queryset.order_by('-payment_date')

    @action(detail=False, methods=['post'], url_path='pay-fees')
    def pay_fees(self, request):
        try:
            student_id = request.data.get('student_id')
            try:
                amount = int(request.data.get('amount', 0))
            except (TypeError, ValueError):
                return error_response("Invalid amount.", code=status.HTTP_400_BAD_REQUEST)
            try:
                method = str(request.data.get('method', 0))
            except (TypeError, ValueError):
                return error_response("Invalid method.", code=status.HTTP_400_BAD_REQUEST)

            remarks = request.data.get('remarks', '')
            try:
                student = Students.objects.get(id=student_id)
            except Students.DoesNotExist:
                return error_response("Student not found.", code=status.HTTP_404_NOT_FOUND)

            # Strict amount check - amount must equal pending_fees
            if(method == 'online'):
                if amount != student.pending_fees:
                    return error_response(
                        f"Payment must be exactly the pending fees: {student.pending_fees}",
                        code=status.HTTP_400_BAD_REQUEST
                    )

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return success_response(
                "Fee payment recorded",
                serializer.data,
                code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return error_response(f"Error creating record: {e}")

    # In fees/views.py - add to FeeHistoryAPI class
    @action(detail=False, methods=['get'], url_path='my-payments')
    def my_payments(self, request):
        """Get payment history for logged-in student"""
        try:
            student_id = request.query_params.get('student_id')  # or get from auth
            if not student_id:
                return error_response("Student ID required")
                
            payments = FeeHistory.objects.filter(student_id=student_id).order_by('-payment_date')
            serializer = self.get_serializer(payments, many=True)
            
            return success_response(
                "Payment history retrieved",
                serializer.data
            )
        except Exception as e:
            return error_response(f"Error fetching payments: {e}")


    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard_stats(self, request):
        try:
            # Total statistics
            total_collected = FeeHistory.objects.filter(status='success').aggregate(
                total=Sum('amount'))['total'] or 0
            
            total_pending = Students.objects.aggregate(
                total=Sum('total_fees'))['total'] or 0
            
            outstanding = total_pending - total_collected
            
            # Monthly collection data (last 6 months)
            six_months_ago = timezone.now() - timedelta(days=180)
            monthly_data = (FeeHistory.objects
                          .filter(status='success', payment_date__gte=six_months_ago)
                          .extra({'month': "strftime('%%Y-%%m', payment_date)"})
                          .values('month')
                          .annotate(total=Sum('amount'), count=Count('id'))
                          .order_by('month'))
            
            # Payment method breakdown
            method_stats = (FeeHistory.objects
                          .filter(status='success')
                          .values('method')
                          .annotate(total=Sum('amount'), count=Count('id')))
            
            dashboard_data = {
                'summary': {
                    'total_collected': total_collected,
                    'total_pending': total_pending,
                    'outstanding': outstanding,
                    'collection_rate': round((total_collected / total_pending * 100), 2) if total_pending > 0 else 0
                },
                'monthly_collections': list(monthly_data),
                'payment_methods': list(method_stats)
            }
            
            return success_response(
                "Dashboard data retrieved successfully",
                dashboard_data
            )
            
        except Exception as e:
            return error_response(f"Error fetching dashboard data: {e}")