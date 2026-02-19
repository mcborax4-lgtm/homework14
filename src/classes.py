import json
from typing import List


class Product:
    """Класс товара"""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс категории"""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)


def load_from_json(file_path: str) -> List[Category]:
    """Загружает категории и товары из JSON-файла"""
    categories = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for cat_data in data:
            products = []
            for prod_data in cat_data["products"]:
                product = Product(
                    prod_data["name"], prod_data["description"], prod_data["price"], prod_data["quantity"]
                )
                products.append(product)

            category = Category(cat_data["name"], cat_data["description"], products)
            categories.append(category)

        print(f"Загружено {len(categories)} категорий")

    except Exception as e:
        print(f"Ошибка загрузки: {e}")

    return categories
