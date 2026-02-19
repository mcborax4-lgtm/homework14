"""
Тесты для классов Product и Category
"""

from src.classes import Category, Product


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
    assert len(category.products) == 2


def test_category_counters():
    """Тест подсчета количества категорий и товаров"""
    # Сбрасываем счетчики
    Category.category_count = 0
    Category.product_count = 0

    # Создаем продукты
    product1 = Product("Телефон", "Смартфон", 50000.0, 10)
    product2 = Product("Ноутбук", "Компьютер", 80000.0, 5)
    product3 = Product("Книга", "Фантастика", 500.0, 20)

    # Создаем категории
    category1 = Category("Электроника", "Гаджеты", [product1, product2])
    category2 = Category("Книги", "Литература", [product3])

    # Проверяем счетчики
    assert Category.category_count == 2
    assert Category.product_count == 3

    # Проверяем что категории создались правильно
    assert category1.name == "Электроника"
    assert category2.name == "Книги"
    assert len(category1.products) == 2
    assert len(category2.products) == 1


def test_product_attributes_types():
    """Тест типов атрибутов продукта"""
    product = Product("Тест", "Описание", 100.0, 5)

    assert isinstance(product.name, str)
    assert isinstance(product.description, str)
    assert isinstance(product.price, float)
    assert isinstance(product.quantity, int)
