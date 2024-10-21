import logging
from collections import deque

# Налаштування логування
logging.basicConfig(level=logging.INFO)

class Order:
    def __init__(self, order_id, customer_name, product_name, quantity):
        self.order_id = order_id
        self.customer_name = customer_name
        self.product_name = product_name
        self.quantity = quantity

    def __repr__(self):
        return f"Order(ID: {self.order_id}, Customer: {self.customer_name}, Product: {self.product_name}, Quantity: {self.quantity})"


class OrderManager:
    def __init__(self):
        self.orders = deque()

    def add_order(self, order_id, customer_name, product_name, quantity):
        try:
            if order_id <= 0:
                raise ValueError("ID замовлення має бути більше 0.")
            if quantity <= 0:
                raise ValueError("Кількість товару має бути більше 0.")
            order = Order(order_id, customer_name, product_name, quantity)
            self.orders.append(order)
            logging.info(f"Замовлення {order_id} додано.")
        except ValueError as e:
            logging.error(f"Помилка додавання замовлення: {e}")
            raise

    def remove_last_order(self):
        if self.orders:
            removed_order = self.orders.pop()
            logging.info(f"Замовлення {removed_order.order_id} видалено.")
        else:
            logging.info("Немає замовлень для видалення.")

    def remove_order_by_id(self, order_id):
        for order in self.orders:
            if order.order_id == order_id:
                self.orders.remove(order)
                logging.info(f"Замовлення {order_id} видалено.")
                return
        logging.info(f"Замовлення з ID {order_id} не знайдено.")

    def find_order_by_id(self, order_id):
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("ID замовлення має бути цілим числом більше 0.")

        for order in self.orders:
            if order.order_id == order_id:
                return order

        raise ValueError(f"Замовлення з ID {order_id} не знайдено.")

    def get_all_orders(self):
        if self.orders:
            logging.info("\nСписок усіх замовлень:")
            for order in self.orders:
                logging.info(order)
        else:
            logging.info("Немає замовлень.")

    def get_order_count(self):
        return len(self.orders)


def menu():
    manager = OrderManager()

    while True:
        print("\n--- Меню ---")
        print("1. Додати нове замовлення")
        print("2. Видалити останнє замовлення")
        print("3. Знайти замовлення за ID")
        print("4. Видалити замовлення за ID")
        print("5. Вивести всі замовлення")
        print("6. Вийти")

        choice = input("Виберіть дію (1-6): ")

        if choice == '1':
            try:
                order_id = int(input("Введіть ID замовлення: "))
                customer_name = input("Введіть ім'я клієнта: ")
                product_name = input("Введіть назву товару: ")
                quantity = int(input("Введіть кількість: "))
                manager.add_order(order_id, customer_name, product_name, quantity)
            except ValueError:
                print("Будь ласка, введіть коректні дані.")

        elif choice == '2':
            manager.remove_last_order()

        elif choice == '3':
            try:
                order_id = int(input("Введіть ID замовлення для пошуку: "))
                order = manager.find_order_by_id(order_id)
                if order:
                    print(f"Знайдено замовлення: {order}")
                else:
                    print("Замовлення з таким ID не знайдено.")
            except ValueError:
                print("Будь ласка, введіть коректний ID.")

        elif choice == '4':
            try:
                order_id = int(input("Введіть ID замовлення для видалення: "))
                manager.remove_order_by_id(order_id)
            except ValueError:
                print("Будь ласка, введіть коректний ID.")

        elif choice == '5':
            manager.get_all_orders()

        elif choice == '6':
            print("Вихід з програми.")
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    menu()
