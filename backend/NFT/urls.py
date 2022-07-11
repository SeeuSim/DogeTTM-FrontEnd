from . import views
from django.urls import path
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('contract/<contract_address>/tokens', cache_page(60*60)(
        views.tokens_by_contract), name="Contract Tokens"),
    path('contract/<contract_address>/price/history/<time_period>/<grouping>', cache_page(60 * 60)(
        views.collection_price_history), name="Contract Price History"),
    path('token/metadata/<contract_address>/<token_id>', cache_page(60*60)(
        views.token_metadata), name="Token Metadata"),
]
