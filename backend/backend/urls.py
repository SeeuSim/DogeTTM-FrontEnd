"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from dashboard import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),  # new
    path('admin/', admin.site.urls),
    # path('top/<param>', views.topSentiments, name= "topSentiments"),
    # path('top/<param>', views.singleCollection, name= "singleCollection")
    path('toprank/<param>', views.topRank, name="topRank"),
    path('toptrend/<period>', views.topTrending, name="topTrending"),
    path('contracts/<contract_id>', views.getContract, name="contract"),
    path('history/price/<contract_address>/<time_period>', views.getPriceHistory, name="priceHistory")
#path TBD
]
