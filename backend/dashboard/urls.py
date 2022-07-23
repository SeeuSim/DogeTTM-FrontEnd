from . import views
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('<metric>/<time_period>/', views.top_collections, name="Top Collections"),
    path('client/<metric>/<time_period>',
        views.top_collections_client, name="Top Collections Client"),
    path('array', lambda request: JsonResponse([1, 2, 3], safe=False), name="Test Array")
]
