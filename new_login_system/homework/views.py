from .models import Homework
from .serializers import HomeworkSerializer
from utils.base_viewsets import BaseCRUDViewSet

class HomeworkViewSet(BaseCRUDViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer