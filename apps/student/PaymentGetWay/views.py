from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView


@permission_classes((permissions.AllowAny,))
class EsewaApi(APIView):
    def post(self, request):
        return Response({'message': 'ok'})


@permission_classes((permissions.AllowAny,))
class KhaltiApi(APIView):
    def post(self, request):
        return Response({'message': 'ok'})
