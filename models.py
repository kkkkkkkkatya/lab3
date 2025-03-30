import hashlib
from typing import List


class User:
    def __init__(self, user_id: int, name: str, email: str, password: str, is_admin: bool = False):
        self.__user_id = user_id  # Приватний атрибут
        self.name = name
        self.email = email
        self.__password = self._hash_password(password)  # Приватний атрибут
        self.is_admin = is_admin
        self.orders: List["Order"] = []

    @staticmethod
    def _hash_password(password: str) -> str:
        """Хешування пароля за допомогою SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self):
        """Реєстрація користувача"""
        print(f"Користувач {self.name} зареєстрований!")

    def login(self, email: str, password: str) -> bool:
        """Авторизація користувача"""
        return self.email == email and self.__password == self._hash_password(password)

    def view_orders(self):
        """Перегляд замовлень користувача"""
        if self.is_admin:
            return "Адміністратор може переглядати всі замовлення."
        return [str(order) for order in self.orders] if self.orders else "Замовлень немає."


class Product:
    def __init__(self, product_id: int, name: str, price: float, stock: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock  # Кількість на складі

    def is_available(self, quantity: int) -> bool:
        """Перевірка доступності товару"""
        return self.stock >= quantity

    def reduce_stock(self, quantity: int):
        """Зменшення кількості товару на складі"""
        if self.is_available(quantity):
            self.stock -= quantity


class Order:
    def __init__(self, order_id: int, user: User):
        self.order_id = order_id
        self.user = user
        self.products: List[dict] = []  # Список товарів у форматі {product: quantity}
        self.status = "Новий"

    def add_product(self, product: Product, quantity: int):
        """Додавання товару в замовлення"""
        if product.is_available(quantity):
            product.reduce_stock(quantity)
            self.products.append({"product": product, "quantity": quantity})
        else:
            print(f"Товар {product.name} недоступний у потрібній кількості.")

    def remove_product(self, product: Product):
        """Видалення товару з замовлення"""
        self.products = [p for p in self.products if p["product"] != product]

    def calculate_total(self) -> float:
        """Розрахунок загальної суми замовлення"""
        return sum(p["product"].price * p["quantity"] for p in self.products)

    def complete_order(self):
        """Завершення замовлення"""
        self.status = "Завершено"
        self.user.orders.append(self)
        print(f"Замовлення {self.order_id} завершено!")



