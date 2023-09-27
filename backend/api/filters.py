<<<<<<< Updated upstream
from django_filters.rest_framework import FilterSet, filters
from products.models import Sales

class SalesFilter(FilterSet):
=======
# import django_filters
# from products.models import Sku

# class SkuFilter(django_filters.FilterSet):
#     pr_group_id = django_filters.CharFilter(field_name='pr_group_id', lookup_expr='startswith')

#     class Meta:
#         model = Sku
#         fields = ['pr_group_id']

from django_filters import rest_framework as filters
from products.models import Sales

class SalesFilter(filters.FilterSet):
>>>>>>> Stashed changes
    st_id = filters.CharFilter()
    pr_sku_id = filters.CharFilter(field_name='pr_sku_id__pr_group_id')
    pr_cat_id = filters.CharFilter(field_name='pr_sku_id__pr_cat_id')
    pr_subcat_id = filters.CharFilter(field_name='pr_sku_id__pr_subcat_id')

    class Meta:
        model = Sales
        fields = ['st_id', 'pr_sku_id', 'pr_cat_id', 'pr_subcat_id']