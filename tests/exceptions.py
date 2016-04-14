from rest_framework.exceptions import APIException, NotFound
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def server_error(request):
    raise APIException('APIException')


@api_view(['GET'])
def not_found(request):
    raise NotFound('NotFound')


@api_view(['POST'])
def method_not_allowed(request):
    pass


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def not_authenticated(request):
    pass
