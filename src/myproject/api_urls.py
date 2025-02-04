from django.urls import path
from app.views import swot_list

urlpatterns = [
    path('swot/', swot_list, name='swot_list'),
]

