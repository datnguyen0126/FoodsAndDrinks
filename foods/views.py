from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from .serializers import FoodSerializer, PostOrPutFoodSerializer, ImagesSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models.CategoryModel import Category
from .models.FoodModel import Food
from .models.ImagesMopdel import Images


class FoodList(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = FoodSerializer

    def get(self, request, format=None):
        foods = Food.objects.all().order_by('-id')
        pagesize = int(settings.PAGESIZE)
        page_total = round(Food.objects.all().count() / pagesize + 0.5)
        paginator = Paginator(foods, pagesize)
        page = request.GET.get("page", "1").isdigit() and int(request.GET.get("page", "1")) or 1
        try:
            paginated_querySet = paginator.page(page)
        except EmptyPage:
            paginated_querySet = paginator.page(paginator.num_pages)
        serializer = self.serializer_class(paginated_querySet, many=True)
        content = {
            "page": page,
            "pagetotal": page_total,
            "listfoods": serializer.data,
        }
        return Response(content)


class CreateFood(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = PostOrPutFoodSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        files = request.FILES.getlist("files")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.files = files
        serializer.save()
        content = {"success": "Create successful food."}
        return Response(content, status=status.HTTP_201_CREATED)


class FoodDetail(APIView):
    serializer_class = FoodSerializer
    permission_classes = [AllowAny, ]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, pk, format=None):
        food = Food.objects.get_object(pk)
        serializer = self.serializer_class(food)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        food = Food.objects.get_object(pk)
        files = request.FILES.getlist("files")
        serializer = PostOrPutFoodSerializer(food, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.files = files
        if serializer.update():
            content = {"success": "Change successful food."}
            return Response(content)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteImagesInFood(APIView):
    permission_classes = [IsAdminUser, ]

    def delete(self, request, pk):
        try:
            Images.objects.get(id=pk).delete()
            content = {"success": "Delete successful images."}
            return Response(content)

        except Images.DoesNotExist:
            raise Http404
