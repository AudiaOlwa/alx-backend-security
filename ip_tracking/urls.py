from django.urls import path
from .views import login_view, public_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponse

schema_view = get_schema_view(
   openapi.Info(
      title="ALX Backend Security API",
      default_version='v1',
      description="API documentation",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

def home_view(request):
    return HttpResponse("Bienvenue sur ALX Backend Security!")

urlpatterns = [
    path('', home_view),
    path('login/', login_view),
    path('public/', public_view),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
