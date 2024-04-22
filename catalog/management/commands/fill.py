import json

from django.core.management import BaseCommand

from catalog.models import Product, Category


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        """Возвращает, список категорий"""
        with open('catalog_Category_data.json', encoding='utf-16') as f:
            result = json.load(f)
            categories_list = []
            for i in result:
                categories_list.append(i)
            return categories_list

    @staticmethod
    def json_read_products():
        """Возвращает, список продуктов"""
        with open('catalog_Product_data.json', encoding='utf-16') as f:
            result = json.load(f)
            products_list = []
            for i in result:
                products_list.append(i)
            return products_list

    def handle(self, *args, **options):
        """Наполняет базу данными из фикстур"""
        # Очищаем таблицы
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(id=category['pk'], name=category['fields']['name'],
                         description=category['fields']['description'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)
        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products():
            product_for_create.append(
                Product(id=product['pk'], category=Category.objects.get(pk=product['fields']['category']),
                        name=product['fields']['name'], price=product['fields']['price'],
                        description=product['fields']['description'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)
