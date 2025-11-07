from django.urls import path
from .views import login_view, public_view

urlpatterns = [
    path('login/', login_view),
    path('public/', public_view),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0))

]
