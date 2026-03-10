from pathlib import Path
from src.classes import Category, load_from_json


def main():
    """Запуск демонстрации"""
    print("=" * 60)
    print("ПРОВЕРКА РАБОТЫ КЛАССОВ")
    print("=" * 60)

    # Сбрасываем счетчики
    Category.category_count = 0
    Category.product_count = 0

    # Загружаем данные
    json_path = Path("data/products.json")

    if json_path.exists():
        categories = load_from_json(str(json_path))

        for category in categories:
            print(f"\n📁 {category.name}")
            print(f"   {category.description}")
            print(f"   Товары:")

            # ✅ Используем итератор (работает через __iter__)
            for product in category:
                print(f"   • {product.name}")
                print(f"     {product.price} руб. | {product.quantity} шт.")
    else:
        print(f"❌ Файл {json_path} не найден")

    print("\n" + "=" * 60)
    print(f"📊 Всего категорий: {Category.category_count}")
    print(f"📊 Всего товаров: {Category.product_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()