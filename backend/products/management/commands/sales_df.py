import csv

from django.core.management.base import BaseCommand
from tqdm import tqdm

from products.models import Sales, Sku, Store, SalesFact
from products.management.setup_logger import setup_logger


logger = setup_logger()


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('products/data/sales_df_train3.csv', encoding='utf-8') as f:
            logger.info('старт загрузки данных')
            reader = csv.reader(f)
            next(reader)
            sales_fact_list = []
            count = 0
            all_stores = Store.objects.all()
            all_sku = Sku.objects.all()
            for row in tqdm(reader):
                try:
                    st_id, pr_sku_id, date, pr_sales_type_id, pr_sales_in_units, pr_promo_sales_in_units, pr_sales_in_rub, pr_promo_sales_in_rub = row
                    store = all_stores.get(pk=st_id)
                    sku = all_sku.get(pk=pr_sku_id)
                    obj, created = Sales.objects.get_or_create(
                        st_id=store,
                        pr_sku_id=sku,
                        date=date,
                    )
                    sale_fact = SalesFact(
                        st_sku_date=obj,
                        sales_type=pr_sales_type_id,
                        sales_units=pr_sales_in_units,
                        sales_units_promo=pr_promo_sales_in_units,
                        sales_rub=pr_sales_in_rub,
                        sales_run_promo=pr_promo_sales_in_rub
                    )
                    sales_fact_list.append(sale_fact)
                    count += 1
                    if count > 9999:
                        SalesFact.objects.bulk_create(sales_fact_list,
                                                      batch_size=1000)
                        logger.info(f'загружено {count} строк')
                        sales_fact_list = []
                        count = 0
                except Exception as error:
                    logger.error(f'сбой в работе: {error}', exc_info=True)
            SalesFact.objects.bulk_create(sales_fact_list, batch_size=1000)
            logger.info(f'загружено {count} строк')
