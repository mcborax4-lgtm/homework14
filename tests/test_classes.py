"""
Тесты для классов Product и Category
"""
import pytest
import json
from src.classes import Category, Product, Smartphone, LawnGrass, load_from_json


# ==== ПРИНУДИТЕЛЬНЫЙ СБРОС СЧЁТЧИКОВ ====
Category.category_count = 0
Category.product_count = 0
# =========================================


@pytest.fixture(autouse=True)
def reset_counters():
    """Сбрасывает счётчики категорий и продуктов перед каждым тестом"""
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
    # Проверяем через приватный атрибут (для тестов)
    assert len(category._Category__products) == 2
    # Проверяем наличие в строковом представлении
    assert "Телефон" in category.products
    assert "Ноутбук" in category.products


def test_category_counters():
    """Тест подсчета количества категорий и товаров"""
    product1 = Product("Телефон", "Смартфон", 50000.0, 10)
    product2 = Product("Ноутбук", "Компьютер", 80000.0, 5)
    product3 = Product("Книга", "Фантастика", 500.0, 20)

    category1 = Category("Электроника", "Гаджеты", [product1, product2])
    category2 = Category("Книги", "Литература", [product3])

    assert Category.category_count == 2
    assert Category.product_count == 3

    assert category1.name == "Электроника"
    assert category2.name == "Книги"
    assert len(category1._Category__products) == 2
    assert len(category2._Category__products) == 1


def test_product_attributes_types():
    """Тест типов атрибутов продукта"""
    product = Product("Тест", "Описание", 100.0, 5)

    assert isinstance(product.name, str)
    assert isinstance(product.description, str)
    assert isinstance(product.price, float)
    assert isinstance(product.quantity, int)


def test_load_from_json_success(tmp_path):
    """Тест успешной загрузки из JSON"""
    json_data = [
        {
            "name": "Тест",
            "description": "Описание",
            "products": [
                {
                    "name": "Товар",
                    "description": "Описание товара",
                    "price": 100.0,
                    "quantity": 5
                }
            ]
        }
    ]

    json_file = tmp_path / "test.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f)

    categories = load_from_json(str(json_file))

    assert len(categories) == 1
    assert categories[0].name == "Тест"
    assert len(categories[0]._Category__products) == 1
    assert categories[0]._Category__products[0].name == "Товар"


def test_load_from_json_file_not_found():
    """Тест при отсутствии файла"""
    categories = load_from_json("nonexistent.json")
    assert categories == []


def test_load_from_json_invalid_format(tmp_path):
    """Тест при неверном формате JSON"""
    json_file = tmp_path / "invalid.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        f.write("это не json")

    categories = load_from_json(str(json_file))
    assert categories == []


def test_load_from_json_missing_keys(tmp_path):
    """Тест при отсутствии обязательных полей"""
    json_data = [{"name": "Тест"}]

    json_file = tmp_path / "missing.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f)

    categories = load_from_json(str(json_file))
    assert categories == []


def test_category_with_empty_products():
    """Тест категории без товаров"""
    category = Category("Пустая", "Нет товаров", [])

    assert category.name == "Пустая"
    assert len(category._Category__products) == 0
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_smartphone_creation():
    """Тест создания смартфона"""
    phone = Smartphone(
        name="iPhone 15",
        description="Флагман Apple",
        price=120000.0,
        quantity=5,
        efficiency=3.2,
        model="15 Pro",
        memory=256,
        color="Серый"
    )

    assert phone.name == "iPhone 15"
    assert phone.price == 120000.0
    assert phone.efficiency == 3.2
    assert phone.model == "15 Pro"
    assert phone.memory == 256
    assert phone.color == "Серый"


def test_lawn_grass_creation():
    """Тест создания газонной травы"""
    grass = LawnGrass(
        name="Газон спортивный",
        description="Быстрорастущий газон",
        price=1500.0,
        quantity=20,
        country="Россия",
        germination_period="7-10 дней",
        color="Зеленый"
    )

    assert grass.name == "Газон спортивный"
    assert grass.price == 1500.0
    assert grass.country == "Россия"
    assert grass.germination_period == "7-10 дней"
    assert grass.color == "Зеленый"


def test_product_str():
    """Тест строкового представления продукта"""
    product = Product("Телефон", "Смартфон", 50000.0, 10)
    assert str(product) == "Телефон, 50000.0 руб. Остаток: 10 шт."


def test_category_str():
    """Тест строкового представления категории"""
    product1 = Product("Телефон", "Смартфон", 50000.0, 10)
    product2 = Product("Ноутбук", "Компьютер", 80000.0, 5)
    category = Category("Электроника", "Гаджеты", [product1, product2])

    expected = "Электроника, количество продуктов: 15 шт."
    assert str(category) == expected


def test_product_add_same_type():
    """Тест сложения продуктов одного типа"""
    a = Product("A", "", 100.0, 2)
    b = Product("B", "", 50.0, 4)
    assert a + b == 400.0


def test_product_add_different_types():
    """Тест сложения продуктов разных типов (должна быть ошибка)"""
    phone = Smartphone("iPhone", "", 100000.0, 2, 3.0, "15", 128, "Черный")
    grass = LawnGrass("Газон", "", 1500.0, 10, "Россия", "7 дней", "Зеленый")

    with pytest.raises(TypeError, match="Нельзя складывать товары разных типов"):
        _ = phone + grass


def test_add_product():
    """Тест добавления продукта в категорию"""
    cat = Category("Книги", "Описание", [])
    p = Product("Книга", "Описание", 500.0, 2)
    cat.add_product(p)

    assert "Книга, 500.0 руб. Остаток: 2 шт." in cat.products


def test_add_product_wrong_type():
    """Тест добавления не-продукта в категорию"""
    cat = Category("Книги", "Описание", [])

    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
        cat.add_product("это строка")


def test_add_product_inherited():
    """Тест добавления наследников Product в категорию"""
    cat = Category("Тест", "Описание", [])
    phone = Smartphone("iPhone", "", 100000.0, 2, 3.2, "15 Pro", 256, "Серый")

    cat.add_product(phone)
    assert "iPhone" in cat.products


def test_price_setter_negative():
    """Тест установки отрицательной цены"""
    product = Product("Тест", "Описание", 100.0, 5)
    product.price = -50
    assert product.price == 100.0


def test_price_setter_positive():
    """Тест установки положительной цены"""
    product = Product("Тест", "Описание", 100.0, 5)
    product.price = 150.0
    assert product.price == 150.0


def test_category_iteration():
    """Тест итерации по товарам категории"""
    product1 = Product("Телефон", "Смартфон", 50000.0, 10)
    product2 = Product("Ноутбук", "Компьютер", 80000.0, 5)
    category = Category("Электроника", "Гаджеты", [product1, product2])

    products_list = []
    for product in category:
        products_list.append(product)

    assert len(products_list) == 2
    assert products_list[0].name == "Телефон"
    assert products_list[1].name == "Ноутбук"