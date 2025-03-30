import unittest
import hashlib
from models import User, Product, Order

class TestEcommerce(unittest.TestCase):
    def setUp(self):
        self.user = User(1, "Alice", "alice@example.com", "password123")
        self.admin = User(2, "Admin", "admin@example.com", "adminpass", is_admin=True)
        self.product1 = Product(101, "Laptop", 1200.00, 10)
        self.product2 = Product(102, "Mouse", 25.00, 5)
        self.order = Order(5001, self.user)

    def test_user_registration(self):
        """Перевірка реєстрації користувача"""
        self.assertEqual(self.user.name, "Alice")
        self.assertEqual(self.user.email, "alice@example.com")

    def test_password_hashing(self):
        """Перевірка хешування пароля"""
        hashed_password = hashlib.sha256("password123".encode()).hexdigest()
        self.assertEqual(self.user._User__password, hashed_password)

    def test_successful_login(self):
        """Перевірка успішного входу"""
        self.assertTrue(self.user.login("alice@example.com", "password123"))

    def test_failed_login(self):
        """Перевірка невдалого входу"""
        self.assertFalse(self.user.login("alice@example.com", "wrongpassword"))

    def test_admin_can_view_orders(self):
        """Перевірка, що адміністратор може переглядати всі замовлення"""
        self.assertEqual(self.admin.view_orders(), "Адміністратор може переглядати всі замовлення.")

    def test_product_availability(self):
        """Перевірка доступності товару"""
        self.assertTrue(self.product1.is_available(5))
        self.assertFalse(self.product2.is_available(10))

    def test_reduce_stock(self):
        """Перевірка зменшення запасу товару після покупки"""
        self.product1.reduce_stock(3)
        self.assertEqual(self.product1.stock, 7)

    def test_add_product_to_order(self):
        """Перевірка додавання товару в замовлення"""
        self.order.add_product(self.product1, 2)
        self.assertEqual(len(self.order.products), 1)
        self.assertEqual(self.product1.stock, 8)

    def test_remove_product_from_order(self):
        """Перевірка видалення товару із замовлення"""
        self.order.add_product(self.product1, 1)
        self.order.remove_product(self.product1)
        self.assertEqual(len(self.order.products), 0)

    def test_calculate_total_price(self):
        """Перевірка підрахунку загальної вартості замовлення"""
        self.order.add_product(self.product1, 1)
        self.order.add_product(self.product2, 2)
        self.assertEqual(self.order.calculate_total(), 1250.00)

    def test_complete_order(self):
        """Перевірка завершення замовлення"""
        self.order.complete_order()
        self.assertEqual(self.order.status, "Завершено")
        self.assertIn(self.order, self.user.orders)

