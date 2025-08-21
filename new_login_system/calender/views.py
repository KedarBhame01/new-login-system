from .models import Calender
from .serializers import CalenderSerializer
from utils.base_viewsets import BaseCRUDViewSet
# Create your views here.
class CalenderViewSet(BaseCRUDViewSet):
    queryset = Calender.objects.all()
    serializer_class = CalenderSerializer