"""
URL configuration for StickerService project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include

from counter.api import DigitCounterView
from stickers.api import StickersSearchView, StickersFeedbackView, StickersStatisticsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/search/', StickersSearchView.as_view(), name='stickers_search'),
    path('api/feedback/', StickersFeedbackView.as_view(), name='stickers_feedback'),
    path('api/analytics/', StickersStatisticsView.as_view(), name='stickers_query_stats'),
    path('api/counter/', DigitCounterView.as_view(), name='counters_digit_counter'),
]
