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
def success_response(message, data=None, code=status.HTTP_200_OK, extra=None):
    response = {
        "status": "success",
        "code": code,
        "message": message,
    }
    if data is not None:
        response["data"] = data
    if extra:
        response.update(extra)
    return Response(response, status=code)


def error_response(message, code=status.HTTP_400_BAD_REQUEST):
    response = {
        "status": "error",
        "code": code,
        "message": message,
    }
    return Response(response, status=code)
# Create your views here.
class FeeHistoryAPI(BaseCRUDViewSet):
    queryset = FeeHistory.objects.all()
    serializer_class = FeeHistorySerializer

    def get_queryset(self):
        student_id = self.request.query_params.get('student_id')
        if student_id:
            return FeeHistory.objects.filter(student_id=student_id)
        return super().get_queryset()

    @action(detail=False, methods=['post'], url_path='pay-fees')
    def pay_fees(self, request):
        try:
            student_id = request.data.get('student_id')
            try:
                amount = int(request.data.get('amount', 0))
            except (TypeError, ValueError):
                return error_response("Invalid amount.", code=status.HTTP_400_BAD_REQUEST)

            remarks = request.data.get('remarks', '')
            try:
                student = Students.objects.get(id=student_id)
            except Students.DoesNotExist:
                return error_response("Student not found.", code=status.HTTP_404_NOT_FOUND)

            # Strict amount check - amount must equal pending_fees
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