import json
from typing import List, Optional
from .abstract_base import BaseProduct
from .mixins import CreationMixin


class Product(CreationMixin, BaseProduct):
    """Класс для описания товара"""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        # Сначала вызываем миксин (через super)
        super().__init__()
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            # Запрашиваем подтверждение
            answer = input(f"Понизить цену с {self.__price} до {new_price}? (y/n): ")
            if answer.lower() == 'y':
                self.__price = new_price
                print("Цена обновлена")
            else:
                print("Отмена понижения цены")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict, existing_products: Optional[list] = None):
        if existing_products:
            for existing in existing_products:
                if existing.name == product_data["name"]:
                    existing.quantity += product_data["quantity"]
                    if product_data["price"] > existing.price:
                        existing.price = product_data["price"]
                    return existing
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только с продуктами")
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов")
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    """Смартфон — наследник Product"""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self) -> str:
        return (
            f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт. "
            f"(Модель: {self.model}, память: {self.memory}ГБ, цвет: {self.color})"
        )


class LawnGrass(Product):
    """Газонная трава — наследник Product"""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        return (
            f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт. "
            f"(Страна: {self.country}, срок прорастания: {self.germination_period})"
        )


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: Optional[list] = None):
        self.name = name
        self.description = description
        self.__products = products if products else []
        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        if not self.__products:
            return "Нет товаров"
        return "\n".join(f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт." for p in self.__products)

    def __str__(self) -> str:
        total = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total} шт."

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index >= len(self.__products):
            raise StopIteration
        product = self.__products[self._index]
        self._index += 1
        return product


def load_from_json(file_path: str) -> List[Category]:
    categories = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for cat_data in data:
            products = [
                Product(p["name"], p["description"], p["price"], p["quantity"])
                for p in cat_data["products"]
            ]
            categories.append(Category(cat_data["name"], cat_data["description"], products))
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
    return categories