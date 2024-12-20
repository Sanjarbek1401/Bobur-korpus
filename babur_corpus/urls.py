from django.contrib import admin
from django.urls import path, include, re_path  # Add re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from main.views import (
    AuthorInfoAPIView,
    BaburnomaAPIView,
    DivanCategoryAPIView,
    DivanGroupAPIView,
    DivanTextAPIView,
    AdminContactAPIView,
    DivanCategoryDetailAPIView,
    DivanGroupDetailAPIView,
    DivanTextDetailAPIView,
    SearchAPIView,
    BaburnomaAPIView,
    BaburnomaDetailAPIView
)

schema_view = get_schema_view(
    openapi.Info(
        title="Babur Corpus API",
        default_version='v1',
        description="API documentation for Babur Corpus project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@baburcorpus.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    # API URLs
    path('api/authors/', AuthorInfoAPIView.as_view(), name='author-info'),
    path('api/boburnoma/', BaburnomaAPIView.as_view(), name='boburnoma_list'),
    path('api/boburnoma/<int:pk>/', BaburnomaDetailAPIView.as_view(), name='boburnoma-detail'),

    path('api/divan-categories/', DivanCategoryAPIView.as_view(), name='divan-categories'),
    path('api/categories/<int:id>/', DivanCategoryDetailAPIView.as_view(), name='divan-category-detail'),

    path('api/divan-groups/', DivanGroupAPIView.as_view(), name='divan-groups'),
    path('api/groups/<int:id>/', DivanGroupDetailAPIView.as_view(), name='divan-group-detail'),
    path('api/divantexts/<int:pk>/', DivanTextDetailAPIView.as_view(), name='divantext-detail'),

    path('api/divan-texts/', DivanTextAPIView.as_view(), name='divan-texts'),
    path('api/contacts/', AdminContactAPIView.as_view(), name='contacts'),
    # API authentication
    path('api-auth/', include('rest_framework.urls')),
    path('api/search/', SearchAPIView.as_view(), name='search-api'),
    # Swagger documentation URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)