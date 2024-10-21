import unittest
from main import OrderManager
import logging

class OrderTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')  # Налаштування формату і рівня
        self.manager = OrderManager()

    def test_add_order(self):
        # Перевірка, чи замовлення додається до списку
        self.manager.add_order(1, "Karasiovich", "Iphone", 2)
        self.assertEqual(len(self.manager.orders), 1)
        self.assertEqual(self.manager.orders[0].customer_name, "Karasiovich")

    def test_add_order_invalid_id(self):
        with self.assertRaises(ValueError) as context:
            self.manager.add_order(0, "Karasiovich", "Iphone", 2)
        self.assertEqual(str(context.exception), "ID замовлення має бути більше 0.")

    def test_remove_last_order(self):
        # Перевірка видалення останнього замовлення
        self.manager.add_order(1, "Karasiovich", "Iphone", 2)
        self.manager.remove_last_order()
        self.assertEqual(len(self.manager.orders), 0)

        # Негативний сценарій: спроба видалення, коли замовлень немає
        with self.assertLogs('root',level='INFO') as log:
            self.manager.remove_last_order()
        self.assertIn("Немає замовлень для видалення.", log.output[-1])

    def test_remove_order_by_id(self):
        self.manager.add_order(1, "Karasiovich", "Iphone", 2)
        self.manager.add_order(2, "Memen", "Iphone", 3)

        with self.assertLogs('root', level='INFO') as log:
            self.manager.remove_order_by_id(1)
        self.assertIn("Замовлення 1 видалено.", log.output[-1])  # Перевірка на позитивний сценарій

        # Негативний сценарій
        with self.assertLogs('root', level='INFO') as log:
            self.manager.remove_order_by_id(99)
        self.assertIn("Замовлення з ID 99 не знайдено.", log.output[-1])

    def test_find_order_by_id(self):
        # Перевірка пошуку замовлення за ID
        self.manager.add_order(1, "Karasiovich", "Iphone", 2)
        found_order = self.manager.find_order_by_id(1)
        self.assertIsNotNone(found_order)
        self.assertEqual(found_order.customer_name, "Karasiovich")

        # Негативний сценарій: пошук неіснуючого замовлення
        with self.assertRaises(ValueError) as context:
            self.manager.find_order_by_id(99)
        self.assertEqual(str(context.exception), "Замовлення з ID 99 не знайдено.")

        # Негативний сценарій: некоректний ID
        with self.assertRaises(ValueError) as context:
            self.manager.find_order_by_id(-1)
        self.assertEqual(str(context.exception), "ID замовлення має бути цілим числом більше 0.")

    def test_get_all_orders(self):
        # Перевірка отримання всіх замовлень
        self.manager.add_order(1, "Karasiovich", "Iphone", 2)
        self.manager.add_order(2, "Memen", "Iphone", 3)

        with self.assertLogs('root',level='INFO') as log:
            self.manager.get_all_orders()
        self.assertIn("Список усіх замовлень:", log.output[0])

    def test_get_order_count(self):
        # Перевірка підрахунку кількості замовлень
        self.manager.add_order(1, "Karasiovich", "Iphone", 2)
        self.assertEqual(self.manager.get_order_count(), 1)
        self.manager.add_order(2, "Memen", "Iphone", 3)
        self.assertEqual(self.manager.get_order_count(), 2)


if __name__ == "__main__":
    unittest.main()
