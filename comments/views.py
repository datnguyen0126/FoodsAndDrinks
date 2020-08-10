from urllib.response import addinfo

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status


class CommentList(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def list(self, request, food_id, *args, **kwargs):
        queryset = Comment.objects.filter(food_id=food_id)
        serializer = CommentDetailSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentDetailSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Comment.objects.filter(user_id=self.request.user, id=self.kwargs['id'])
