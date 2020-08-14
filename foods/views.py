import math
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from .serializers import FoodSerializer, PostOrPutFoodSerializer, RatingSerializer, CategorySerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from .models.CategoryModel import Category
from .models.FoodModel import Food
from .models.ImagesMopdel import Images
from .models.RatingModel import Rating
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class CategoryList(ListCreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = CategorySerializer


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Category.objects.filter(id=self.kwargs['id'])


class FoodList(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = FoodSerializer

    def get(self, request, format=None):
        foods = Food.objects.all().order_by('-id')
        pagesize = int(settings.PAGESIZE)
        page_total = math.ceil(len(foods) / pagesize)
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


class FoodListByCategory(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = FoodSerializer

    def get(self, request, pk, format=None):
        foods = Food.objects.filter(category_id=pk).order_by('-id')
        pagesize = int(settings.PAGESIZE)
        page_total = math.ceil(len(foods) / pagesize)
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


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def delete(self, request, *args, **kwargs):
        response = {'message': 'Rating cannot be delete like this'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        response = {'message': 'Rating cannot be update like this'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
