from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .documents import FoodDocument
from foods.serializers import FoodSerializer


class SearchList(APIView):
    permission_classes = [AllowAny]
    serializer_class = FoodSerializer

    def post(self, request, format=None):
        if request.data.get('q'):
            foods = FoodDocument.search().query("multi_match", query=request.data.get('q')).to_queryset()
            serializer = self.serializer_class(foods, many=True)
            return Response({"results": serializer.data})
        return Response({"results": []})
