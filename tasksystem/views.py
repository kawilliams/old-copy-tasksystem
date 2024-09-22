from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from asgiref.sync import sync_to_async

# just a keepalive message
class Root(APIView):
  permission_classes = (AllowAny,)

  @sync_to_async
  def get(self, request):
    return JsonResponse({"status": "ok"})

