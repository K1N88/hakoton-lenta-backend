from datetime.date import today

from django.db.models import Max
from rest_framework import serializers

from products.models import Sku, Store, Forecast, SalesFact, Sales


class SkuSerializer(serializers.ModelSerializer):
    ''''Сериализатор для модели Товар'''
    pr_sku_id = serializers.CharField(max_length=200)
    pr_group_id = serializers.CharField(max_length=200)
    pr_cat_id = serializers.CharField(max_length=200)
    pr_subcat_id = serializers.CharField(max_length=200)
    pr_uom_id = serializers.IntegerField()

    class Meta:
        model = Sku
        fields = ('pr_sku_id', 'pr_group_id', 'pr_cat_id', 'pr_subcat_id',
                  'pr_uom_id',)


class StoreSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Магазины'''
    st_id = serializers.CharField(max_length=200)
    st_city_id = serializers.CharField(max_length=200)
    st_division_code = serializers.CharField(max_length=200)
    st_type_format_id = serializers.IntegerField()
    st_type_loc_id = serializers.IntegerField()
    st_type_size_id = serializers.IntegerField()
    st_is_active = serializers.IntegerField()

    class Meta:
        model = Store
        fields = ('st_id', 'st_city_id', 'st_division_code',
                  'st_type_format_id', 'st_type_loc_id', 'st_type_size_id',
                  'st_is_active',)


class ForecastSkuSerializer(serializers.ModelSerializer):
    date = serializers.CharField(source='st_sku_date.date')

    class Meta:
        model = Forecast
        fields = ('date', 'sales_units',)


class ForecastSerializer(serializers.ModelSerializer):
    '''Сериализатор для страницы с прогнозом продаж'''
    store = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_sku_date.st_id'
    )
    group = serializers.CharField(
        source='st_sku_date.pr_sku_id.pr_group_id'
    )
    category = serializers.CharField(
        source='st_sku_date.pr_sku_id.pr_cat_id'
    )
    subcategory = serializers.CharField(
        source='st_sku_date.pr_sku_id.pr_subcat_id'
    )
    sku = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_sku_date.pr_sku_id'
    )
    forecast = serializers.SerializerMethodField()

    class Meta:
        model = Forecast
        fields = ('store', 'group', 'category', 'subcategory',
                  'sku', 'forecast',)

    def get_forecast(self, obj):
        last_forecast = Forecast.objects.aggregate(
            Max('forecast_date')
        )['forecast_date__max']
        forecast = Forecast.objects.filter(
            forecast_date=last_forecast,
            st_sku_date__st_id=obj.st_sku_date.st_id,
            st_sku_date__pr_sku_id=obj.st_sku_date.pr_sku_id
        )
        return ForecastSkuSerializer(forecast, many=True).data


class ForecastPostSerializer(serializers.ModelSerializer):
    st_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_id',
    )
    pr_sku_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='pr_sku_id',
    )
    date = serializers.DateField()
    target = serializers.DecimalField(max_digits=6, decimal_places=1)

    class Meta:
        model = Forecast
        fields = ('store', 'sku', 'forecast_date', 'forecast')

    def create(self, validated_data):
        obj, created = Sales.objects.get_or_create(
            st_id=validated_data['st_id'],
            pr_sku_id=validated_data['pr_sku_id'],
            date=validated_data['date'],
        )
        forecast = Forecast.objects.create(
            st_sku_date=obj,
            sales_units=validated_data['target'],
            forecast_date=today(),
        )
        return forecast


class SalesSerializer(serializers.ModelSerializer):
    '''Сериализатор факта продаж'''
    store = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_sku_date.st_id'
    )
    sku = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_sku_date.pr_sku_id'
    )
    date = serializers.DateTimeField(
        source='st_sku_date.date',
        read_only=True,
    )

    class Meta:
        model = SalesFact
        fields = ('store', 'sku', 'date', 'sales_type', 'sales_units',
                  'sales_units_promo', 'sales_rub', 'sales_run_promo')


class SalesPostSerializer(serializers.ModelSerializer):
    '''Сериализатор загрузки факта продаж.'''
    st_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_sku_date.st_id'
    )
    pr_sku_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='st_sku_date.pr_sku_id'
    )
    date = serializers.DateField()
    pr_sales_type_id = serializers.IntegerField(min_value=0, max_value=1)
    pr_sales_in_units = serializers.DecimalField(max_digits=6,
                                                 decimal_places=1)
    pr_promo_sales_in_units = serializers.DecimalField(max_digits=6,
                                                       decimal_places=1)
    pr_sales_in_rub = serializers.DecimalField(max_digits=8, decimal_places=1)
    pr_promo_sales_in_rub = serializers.DecimalField(max_digits=8,
                                                     decimal_places=1)

    class Meta:
        model = SalesFact
        fields = ('st_id', 'pr_sku_id', 'date', 'pr_sales_type_id',
                  'pr_sales_in_units', 'pr_promo_sales_in_units',
                  'pr_sales_in_rub', 'pr_promo_sales_in_rub')

    def create(self, validated_data):
        obj, created = Sales.objects.get_or_create(
            st_id=validated_data['st_id'],
            pr_sku_id=validated_data['pr_sku_id'],
            date=validated_data['date'],
        )
        sale = SalesFact.objects.create(
            st_sku_date=obj,
            sales_type=validated_data['pr_sales_type_id'],
            sales_units=validated_data['pr_sales_in_units'],
            sales_units_promo=validated_data['pr_promo_sales_in_units'],
            sales_rub=validated_data['pr_sales_in_rub'],
            sales_run_promo=validated_data['pr_promo_sales_in_rub'],
        )
        return sale
