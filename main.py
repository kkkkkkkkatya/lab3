from models import User, Product, Order


if __name__ == "__main__":
    # Run script for testing all class methods

    # Create Users
    user1 = User(1, "Alice", "alice@example.com", "securepassword")
    admin = User(2, "Admin", "admin@example.com", "adminpass", is_admin=True)

    # Register Users
    user1.register()
    admin.register()

    # Login Attempt
    print("\nLogin Test:")
    print("User1 login success:", user1.login("alice@example.com", "securepassword"))  # Should be True
    print("Admin login success:", admin.login("admin@example.com", "wrongpass"))  # Should be False

    # Create Products
    product1 = Product(101, "Laptop", 1200.00, 10)
    product2 = Product(102, "Mouse", 25.00, 50)

    # Check product availability
    print("\nProduct Availability:")
    print(f"Is {product1.name} available (5 units)?", product1.is_available(5))  # True
    print(f"Is {product2.name} available (60 units)?", product2.is_available(60))  # False

    # Create Order
    order1 = Order(5001, user1)

    # Add Products to Order
    order1.add_product(product1, 2)  # Reduces stock by 2
    order1.add_product(product2, 1)  # Reduces stock by 1
    order1.add_product(product2, 60)  # Not enough stock (should print warning)

    # View Order Details
    print("\nOrder Details:")
    for item in order1.products:
        print(f"{item['product'].name} - {item['quantity']} pcs")

    # Calculate Total Price
    print("\nTotal Order Cost:", order1.calculate_total())

    # Complete Order
    order1.complete_order()

    # View Orders (User)
    print("\nUser's Orders:", user1.view_orders())

    # Admin Viewing All Orders
    print("\nAdmin View Orders:", admin.view_orders())

