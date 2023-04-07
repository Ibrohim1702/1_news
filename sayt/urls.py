from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name="home"),
    path('ctg/<key>/', category, name="ctg"),
    path('cnt/', contact, name="cnt"),
    path('s/', search, name="search"),
    path('view/<int:pk>/', view, name="view"),
]