import json
from typing import List, Optional


class Product:
    """Класс для описания товара"""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            # Дополнительное задание подтверждение понижения цены
            answer = input(f"Понизить цену с {self.__price} до {new_price}? (y/n): ")
            if answer.lower() == "y":
                self.__price = new_price
                print("Цена обновлена")
            else:
                print("Отмена понижения цены")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict, existing_products: Optional[list] = None):
        """
        Создаёт новый продукт из словаря с проверкой дубликатов
        """
        # Проверяем дубликаты, если передан список
        if existing_products:
            for existing in existing_products:
                if existing.name == product_data["name"]:
                    # Товар уже существует — обновляем количество и цену
                    existing.quantity += product_data["quantity"]
                    if product_data["price"] > existing.price:
                        existing.price = product_data["price"]
                    return existing

        # Если дубликатов нет - создаём новый
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )


class Category:
    """Класс для описания категории товаров"""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: Optional[list] = None):
        self.name = name
        self.description = description
        self.__products = products if products else []  # Приватный атрибут

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: "Product") -> None:
        """Добавляет товар в категорию"""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает строку со списком товаров"""
        if not self.__products:
            return "Нет товаров"

        result = []
        for product in self.__products:
            result.append(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.")

        return "\n".join(result)


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
