from rest_framework import viewsets, filters
from explorerestaurants import serializers, models
from .serializers import RestaurantInfoSerializer, MenuInfoSerializer
from .models import RestaurantInfo, MenuInfo
from rest_framework.parsers import FileUploadParser


class RestaurantInfoViewSet(viewsets.ModelViewSet):
    queryset = RestaurantInfo.objects.all().order_by('name')
    serializer_class = RestaurantInfoSerializer
    parser_class = (FileUploadParser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','location',)
    http_method_names = ['get']

class MenuInfoViewSet(viewsets.ModelViewSet):
    queryset = MenuInfo.objects.all().order_by('item_name')
    serializer_class = MenuInfoSerializer
    parser_class = (FileUploadParser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('item_name', 'price',) 
    http_method_names = ['get']   