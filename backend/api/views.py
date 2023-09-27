from rest_framework import viewsets
from products.models import Sku, Sales, Store
from api.serializers import SkuSerializer, SalesSerializer, StoreSerializer



class SkuViewSet(viewsets.ReadOnlyModelViewSet):
    '''Обработчик для товаров.'''
    queryset = Sku.objects.all()
    serializer_class = SkuSerializer


class SalesViewSet(viewsets.ReadOnlyModelViewSet):
    '''Обработчик для фактических продаж.'''
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SalesFilter

class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    '''Обработчик для магазинов.'''
    queryset = Store.objects.all()
    serializer_class = StoreSerializer 