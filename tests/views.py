from rest_framework.mixins import (ListModelMixin, CreateModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)
from rest_framework.generics import GenericAPIView

from tests.models import Snippet
from tests.serializers import (SnippetModelSerializer,
                               AnotherSnippetModelSerializer)


class SnippetList(ListModelMixin,
                  CreateModelMixin,
                  GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Snippet2List(ListModelMixin,
                   CreateModelMixin,
                   GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = AnotherSnippetModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SnippetDetail(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
