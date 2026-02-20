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


def test_load_from_json_success(tmp_path):
    """Тест успешной загрузки из JSON"""
    # Создаем временный JSON
    json_data = [
        {
            "name": "Тест",
            "description": "Описание",
            "products": [{"name": "Товар", "description": "Описание товара", "price": 100.0, "quantity": 5}],
        }
    ]

    import json

    json_file = tmp_path / "test.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f)

    from src.classes import load_from_json

    categories = load_from_json(str(json_file))

    assert len(categories) == 1
    assert categories[0].name == "Тест"
    assert len(categories[0].products) == 1
    assert categories[0].products[0].name == "Товар"


def test_load_from_json_file_not_found():
    """Тест при отсутствии файла"""
    from src.classes import load_from_json

    categories = load_from_json("nonexistent.json")
    assert categories == []


def test_load_from_json_invalid_format(tmp_path):
    """Тест при неверном формате JSON"""
    json_file = tmp_path / "invalid.json"
    with open(json_file, "w", encoding="utf-8") as f:
        f.write("это не json")

    from src.classes import load_from_json

    categories = load_from_json(str(json_file))
    assert categories == []


def test_load_from_json_missing_keys(tmp_path):
    """Тест при отсутствии обязательных полей"""
    json_data = [{"name": "Тест"}]  # нет products

    import json

    json_file = tmp_path / "missing.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f)

    from src.classes import load_from_json

    categories = load_from_json(str(json_file))
    assert categories == []


def test_category_with_empty_products():
    """Тест категории без товаров"""
    Category.category_count = 0
    Category.product_count = 0

    category = Category("Пустая", "Нет товаров", [])

    assert category.name == "Пустая"
    assert len(category.products) == 0
    assert Category.category_count == 1
    assert Category.product_count == 0
