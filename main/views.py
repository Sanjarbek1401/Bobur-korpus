from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import DivanCategoryFilter
from .models import *
from .serializers import *
from drf_yasg import openapi
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.db.models import Q
from rest_framework.generics import RetrieveAPIView

class AuthorInfoAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(operation_description="Get author information")
    def get(self, request, *args, **kwargs):
        authors = AuthorInfo.objects.all()
        serializer = AuthorInfoSerializer(authors, many=True)
        return Response(serializer.data)


class BaburnomaAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        boburnoma_list = Baburnoma.objects.all()
        serializer = BaburnomaSerializer(boburnoma_list, many=True, context ={"request":request})
        return Response(serializer.data)
    
class BaburnomaDetailAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Baburnoma.objects.all()
    serializer_class = BaburnomaSerializer


class DivanCategoryAPIView(APIView):
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DivanCategoryFilter
    search_fields = ['name', 'groups__name', 'groups__texts__text']

    @swagger_auto_schema(
        operation_description="""List and search Divan categories.""",
        manual_parameters=[
            openapi.Parameter(
                'group_name',
                openapi.IN_QUERY,
                description="Filter by Divan Group name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'text_content',
                openapi.IN_QUERY,
                description="Filter by text content",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = DivanCategory.objects.prefetch_related(
            'groups', 'groups__texts'  # little_groups olib tashlandi
        ).distinct()
        queryset = self.filter_queryset(queryset)
        serializer = DivanCategorySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        search_backend = filters.SearchFilter()
        return search_backend.filter_queryset(self.request, queryset, view=self)

class DivanCategoryDetailAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific Divan category by ID, including image."
    )
    def get(self, request, id, *args, **kwargs):
        try:
            category = DivanCategory.objects.prefetch_related(
                'groups', 'groups__texts'
            ).get(id=id)
        except DivanCategory.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DivanCategorySerializer(category, context={'request': request})
        return Response(serializer.data)


class DivanGroupAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        groups = DivanGroup.objects.all()
        serializer = DivanGroupSerializer(groups, many=True)
        return Response(serializer.data)


class DivanGroupDetailAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific Divan group by ID, including associated DivanText objects."
    )
    def get(self, request, id, *args, **kwargs):
        try:
            group = DivanGroup.objects.prefetch_related('texts').get(id=id)
        except DivanGroup.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DivanGroupSerializer(group)
        return Response(serializer.data)


class DivanTextAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        texts = DivanText.objects.all()
        serializer = DivanTextSerializer(texts, many=True)
        return Response(serializer.data)


class DivanTextDetailAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk, *args, **kwargs):
        try:
            # ID orqali DivanText ob'ektini olish
            text = DivanText.objects.get(pk=pk)
        except DivanText.DoesNotExist:
            raise NotFound(detail="DivanText with the given ID does not exist.", code=status.HTTP_404_NOT_FOUND)

        # Serializerni ishlatib DivanText ob'ektini JSON formatida qaytarish
        serializer = DivanTextSerializer(text)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', None)

        if query:
            # DivanCategory dan qidirish
            category_results = DivanCategory.objects.filter(Q(name__icontains=query))
            category_serializer = DivanCategorySerializer(category_results, many=True)

            # DivanGroup dan qidirish
            group_results = DivanGroup.objects.filter(Q(name__icontains=query))
            group_serializer = DivanGroupSerializer(group_results, many=True)

            # DivanText dan qidirish
            text_results = DivanText.objects.filter(Q(text__icontains=query))
            text_serializer = DivanTextSerializer(text_results, many=True)

            # Natijalarni JSON formatida birlashtirish
            data = {
                'categories': category_serializer.data,
                'groups': group_serializer.data,
                'texts': text_serializer.data,
            }

            return Response(data)

        return Response({'message': 'Qidiruv so\'zi kiritilmagan.'})

class AdminContactAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        contacts = AdminContact.objects.all()
        serializer = AdminContactSerializer(contacts, many=True)
        return Response(serializer.data)
