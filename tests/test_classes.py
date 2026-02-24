"""
Тесты для классов Product и Category
"""

import json

import pytest

from src.classes import Category, Product, load_from_json


@pytest.fixture(autouse=True)
def reset_counters():
    """Сбрасывает счетчики перед каждым тестом"""
    Category.category_count = 0
    Category.product_count = 0
    yield


def test_product_initialization():
    """Тест инициализации продукта"""
    product = Product("Телефон", "Смартфон", 50000.0, 10)

    assert product.name == "Телефон"
    assert product.description == "Смартфон"
    assert product.price == 50000.0
    assert product.quantity == 10


def test_category_initialization():
    """Тест инициализации категории"""
    product1 = Product("Телефон", "Смартфон", 50000.0, 10)
    product2 = Product("Ноутбук", "Компьютер", 80000.0, 5)

    category = Category("Электроника", "Товары для дома", [product1, product2])

    assert category.name == "Электроника"
    assert category.description == "Товары для дома"
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_category_counters():
    """Тест подсчета количества категорий и товаров"""
    # Принудительный сброс счетчиков
    Category.category_count = 0
    Category.product_count = 0

    product1 = Product("Телефон", "Смартфон", 50000.0, 10)
    product2 = Product("Ноутбук", "Компьютер", 80000.0, 5)
    product3 = Product("Книга", "Фантастика", 500.0, 20)

    category1 = Category("Электроника", "Гаджеты", [product1, product2])
    category2 = Category("Книги", "Литература", [product3])

    assert Category.category_count == 2
    assert Category.product_count == 3

    # Проверяем длину списка товаров через приватный атрибут (для теста)
    assert len(category1._Category__products) == 2
    assert len(category2._Category__products) == 1

    # Проверяем что строковое представление работает
    assert "Телефон" in category1.products
    assert "Ноутбук" in category1.products
    assert "Книга" in category2.products


def test_product_attributes_types():
    """Тест типов атрибутов продукта"""
    product = Product("Тест", "Описание", 100.0, 5)

    assert isinstance(product.name, str)
    assert isinstance(product.description, str)
    assert isinstance(product.price, float)
    assert isinstance(product.quantity, int)


def test_load_from_json_success(tmp_path):
    """Тест успешной загрузки из JSON"""
    # Принудительный сброс счетчиков
    Category.category_count = 0
    Category.product_count = 0

    json_data = [
        {
            "name": "Тестовая категория",
            "description": "Описание категории",
            "products": [{"name": "Тестовый товар", "description": "Описание товара", "price": 100.0, "quantity": 5}],
        }
    ]

    json_file = tmp_path / "test.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f)

    categories = load_from_json(str(json_file))

    assert len(categories) == 1
    assert categories[0].name == "Тестовая категория"

    # Проверяем через приватный атрибут
    assert len(categories[0]._Category__products) == 1
    assert categories[0]._Category__products[0].name == "Тестовый товар"

    # Проверяем счетчики
    assert Category.category_count == 1
    assert Category.product_count == 1


def test_load_from_json_file_not_found():
    """Тест при отсутствии файла"""
    categories = load_from_json("nonexistent.json")
    assert categories == []


def test_load_from_json_invalid_format(tmp_path):
    """Тест при неверном формате JSON"""
    json_file = tmp_path / "invalid.json"
    with open(json_file, "w", encoding="utf-8") as f:
        f.write("это не json")

    categories = load_from_json(str(json_file))
    assert categories == []


def test_category_with_empty_products():
    """Тест категории без товаров"""
    category = Category("Пустая", "Нет товаров", [])

    assert category.name == "Пустая"
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_new_product_classmethod():
    """Тест класс-метода new_product"""
    data = {"name": "Новый товар", "description": "Описание", "price": 200.0, "quantity": 10}

    product = Product.new_product(data)

    assert product.name == "Новый товар"
    assert product.price == 200.0
    assert product.quantity == 10


def test_new_product_with_duplicates():
    """Тест создания продукта с проверкой дубликатов"""
    # Создаем существующий продукт
    existing_product = Product("Телефон", "Старый", 50000.0, 10)
    existing_products = [existing_product]

    # Пытаемся создать такой же
    data = {"name": "Телефон", "description": "Новый", "price": 55000.0, "quantity": 5}

    result = Product.new_product(data, existing_products)

    # Должен вернуться существующий продукт с обновленными данными
    assert result is existing_product
    assert result.quantity == 15  # 10 + 5
    assert result.price == 55000.0  # взяли бОльшую цену


def test_new_product_with_duplicates_lower_price():
    """Тест создания продукта с дубликатом, но меньшей ценой"""
    existing_product = Product("Телефон", "Старый", 50000.0, 10)
    existing_products = [existing_product]

    data = {"name": "Телефон", "description": "Новый", "price": 45000.0, "quantity": 5}  # цена меньше

    result = Product.new_product(data, existing_products)

    # Цена не должна понизиться
    assert result.price == 50000.0
    assert result.quantity == 15


def test_new_product_without_duplicates():
    """Тест создания нового продукта без дубликатов"""
    data = {"name": "Планшет", "description": "Новый", "price": 30000.0, "quantity": 7}

    result = Product.new_product(data)

    assert result.name == "Планшет"
    assert result.price == 30000.0
    assert result.quantity == 7


def test_price_setter_negative(monkeypatch):
    """Тест установки отрицательной цены"""
    product = Product("Тест", "Описание", 100.0, 5)

    # Мокаем input чтобы не ждать ввода
    monkeypatch.setattr("builtins.input", lambda _: "n")

    product.price = -50
    assert product.price == 100.0  # цена не изменилась


def test_price_setter_decrease_confirmed(monkeypatch):
    """Тест понижения цены с подтверждением"""
    product = Product("Тест", "Описание", 100.0, 5)

    # Подтверждаем понижение
    monkeypatch.setattr("builtins.input", lambda _: "y")

    product.price = 80.0
    assert product.price == 80.0


def test_price_setter_decrease_canceled(monkeypatch):
    """Тест отмены понижения цены"""
    product = Product("Тест", "Описание", 100.0, 5)

    # Отменяем понижение
    monkeypatch.setattr("builtins.input", lambda _: "n")

    product.price = 80.0
    assert product.price == 100.0  # цена не изменилась


def test_add_product_method():
    """Тест метода add_product"""
    category = Category("Тест", "Описание", [])
    product = Product("Новый", "Товар", 100.0, 5)

    category.add_product(product)

    assert len(category._Category__products) == 1
    assert category._Category__products[0].name == "Новый"
    assert Category.product_count == 1


def test_products_property_empty():
    """Тест геттера products для пустой категории"""
    category = Category("Пустая", "Нет товаров", [])
    assert category.products == "Нет товаров"


def test_products_property_with_products():
    """Тест геттера products с товарами"""
    product = Product("Телефон", "Смартфон", 50000.0, 10)
    category = Category("Электроника", "Гаджеты", [product])

    expected = "Телефон, 50000.0 руб. Остаток: 10 шт."
    assert expected in category.products
