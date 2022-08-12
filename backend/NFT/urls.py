from functools import cache
from . import views
from django.urls import path
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('contract/<contract_address>', cache_page(60*60)(
        views.contract), name="Contract"),
    path('contract/<contract_address>/tokens', cache_page(60*60)(
        views.tokens_by_contract), name="Contract Tokens"),
    path('contract/<contract_address>/price/history/<time_period>/<grouping>', cache_page(60 * 60)(
        views.collection_price_history_with_sentiment), name="Contract Price History with Sentiment"),
    path('token/metadata/<contract_address>/<token_id>', cache_page(60*60)(
        views.token_metadata), name="Token Metadata"),

    path('dashboard_ranking/<metric>/<time_period>', cache_page(60)(views.dashboard_ranking), name="Dashboard Ranking"),
    path('collection/<contract_address>', cache_page(60)(views.CollectionView.collection_page), name="Collection Details"),
    path('search/<search_field>/<param>', cache_page(60)(views.search_collections), name="Search for collections")
]
