from django.db import models


class Sku(models.Model):
    '''Товар'''
    pr_sku_id = models.CharField(
        primary_key=True,
        max_length=200,
        verbose_name='Товар',
        db_index=True,
    )
    pr_group_id = models.CharField(
        max_length=200,
        verbose_name='Группа',
    )
    pr_cat_id = models.CharField(
        max_length=200,
        verbose_name='Категория',
    )
    pr_subcat_id = models.CharField(
        max_length=200,
        verbose_name='Подкатегория',
    )
    pr_uom_id = models.IntegerField(verbose_name='Единицы измерения',)


class Store(models.Model):
    '''Магазин'''
    st_id = models.CharField(
        primary_key=True,
        max_length=200,
        verbose_name='магазин',
        db_index=True,
    )
    st_city_id = models.CharField(
        max_length=200,
        verbose_name='город',
    )
    st_division_code = models.CharField(
        max_length=200,
        verbose_name='дивизион',
    )
    st_type_format_id = models.IntegerField(verbose_name='формат',)
    st_type_loc_id = models.IntegerField(verbose_name='тип локации/окружения',)
    st_type_size_id = models.IntegerField(verbose_name='размер',)
    st_is_active = models.IntegerField(verbose_name='активность',)


class ForecastSku(models.Model):
    '''Дата прогноза'''
    st_id = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='forecast_store',
        verbose_name='магазин',
    )
    pr_sku_id = models.ForeignKey(
        Sku,
        on_delete=models.CASCADE,
        related_name='forecast_sku',
        verbose_name='товар',
    )
    forecast_date = models.DateTimeField(verbose_name='Дата прогноза',)

    class Meta:
        verbose_name = 'прогноз'
        verbose_name_plural = 'прогнозы'

    def __str__(self):
        return f'''Прогноз для {self.store_sku_id} на {self.forecast_date}'''


class Forecast(models.Model):
    '''Прогнозы'''
    date = models.DateTimeField(verbose_name='дата прогноза',)
    target = models.IntegerField(verbose_name='цель',)
    forecast_sku_id = models.ForeignKey(
        ForecastSku,
        on_delete=models.CASCADE,
        related_name='forecast',
    )

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'''Прогноз для {self.forecast_sku_id}
                   на {self.date}'''


class Sales(models.Model):
    '''Продажи факт'''
    st_id = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='sales_store',
        verbose_name='магазин',
    )
    pr_sku_id = models.ForeignKey(
        Sku,
        on_delete=models.CASCADE,
        related_name='sales_sku',
        verbose_name='товар',
    )
    date = models.DateTimeField(verbose_name='дата прогноза',)
    sales_type = models.IntegerField(verbose_name='тип продаж',)
    sales_units = models.IntegerField(verbose_name='всего шт',)
    sales_units_promo = models.IntegerField(verbose_name='промо шт',)
    sales_rub = models.DecimalField(verbose_name='всего руб',)
    sales_run_promo = models.DecimalField(verbose_name='промо руб',)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'Факт продаж для {self.sales_sku_id} на {self.date}'