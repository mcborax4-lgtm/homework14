"""
Миксин для логирования создания объектов
"""


class CreationMixin:
    """
    Миксин, который при создании объекта печатает информацию о нём.
    """

    def __init__(self, *args, **kwargs):
        # Печатаем информацию о создании
        print(f"Создан объект {self.__class__.__name__} с параметрами: {self.__dict__}")

    def __repr__(self) -> str:
        """Для красивого вывода в консоль"""
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"
