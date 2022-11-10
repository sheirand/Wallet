from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Wallet API",
        default_version='v1',
        description="Application made for tracking your transactions",
        contact=openapi.Contact(email="eugene.osakovich@gmail.com"),
        license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('schema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-wallet-api'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
