from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

# just a keepalive message
class Root(APIView):
  permission_classes = (AllowAny,)
  def get(self, request):
    return JsonResponse({"status": "ok"})

