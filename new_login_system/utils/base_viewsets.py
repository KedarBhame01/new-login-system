from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
# from utils.responses import success_response, error_response


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


class BaseCRUDViewSet(ModelViewSet):
    """
    A reusable base CRUD class with standard response format.
    Any new API can just inherit this and set queryset + serializer_class.
    """

    # ✅ List
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return success_response("All records fetched", serializer.data)
        except Exception as e:
            return error_response(f"Error fetching list: {e}", code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ✅ Retrieve
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return success_response("Record fetched successfully", serializer.data)
        except Exception as e:
            return error_response(f"Error fetching record: {e}", code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ✅ Create
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response("Record created successfully",
                                    serializer.data,
                                    code=status.HTTP_201_CREATED)
        except Exception as e:
            return error_response(f"Error creating record: {e}")

    # ✅ Update
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response("Record updated successfully", serializer.data)
        except Exception as e:
            return error_response(f"Error updating record: {e}")

    # ✅ Partial Update
    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response("Record partially updated successfully", serializer.data)
        except Exception as e:
            return error_response(f"Error in partial update: {e}")

    # ✅ Destroy
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return success_response("Record deleted successfully")
        except Exception as e:
            return error_response(f"Error deleting record: {e}")


