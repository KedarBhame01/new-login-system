from .models import Notices
from .serializers import NoticeSerializerserializer
from utils.base_viewsets import BaseCRUDViewSet
# Create your views here.
class NoticeViewSet(BaseCRUDViewSet):
    queryset = Notices.objects.all().order_by('-created_at')
    serializer_class = NoticeSerializerserializer