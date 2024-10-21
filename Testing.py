import unittest
import xmlrunner
from main import OrderManager
import os
import logging

class OrderTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')  # Налаштування формату і рівня
        self.manager = OrderManager()

    def test_add_order(self):
        self.manager.add_order(1, "Karasiovich", "Iphone", 2)
        self.assertEqual(len(self.manager.orders), 1)
        self.assertEqual(self.manager.orders[0].customer_name, "Karasiovich")

    def test_add_order_invalid_id(self):
        with self.assertRaises(ValueError) as context:
            self.manager.add_order(0, "Karasiovich", "Iphone", 2)
        self.assertEqual(str(context.exception), "ID замовлення має бути більше 0.")

    def test_remove_last_order(self):
        self.manager.add_order(1, "Karasiovich", "Iphone", 2)
        self.manager.remove_last_order()
        self.assertEqual(len(self.manager.orders), 0)

        with self.assertLogs('root',level='INFO') as log:
            self.manager.remove_last_order()
        self.assertIn("Немає замовлень для видалення.", log.output[-1])

    def test_remove_order_by_id(self):
        self.manager.add_order(1, "Karasiovich", "Iphone", 2)
        self.manager.add_order(2, "Memen", "Iphone", 3)

        with self.assertLogs('root', level='INFO') as log:
            self.manager.remove_order_by_id(1)
        self.assertIn("Замовлення 1 видалено.", log.output[-1])  # Перевірка на позитивний сценарій

        with self.assertLogs('root', level='INFO') as log:
            self.manager.remove_order_by_id(99)
        self.assertIn("Замовлення з ID 99 не знайдено.", log.output[-1])

    def test_find_order_by_id(self):
        self.manager.add_order(1, "Karasiovich", "Iphone", 2)
        found_order = self.manager.find_order_by_id(1)
        self.assertIsNotNone(found_order)
        self.assertEqual(found_order.customer_name, "Karasiovich")

        with self.assertRaises(ValueError) as context:
            self.manager.find_order_by_id(99)
        self.assertEqual(str(context.exception), "Замовлення з ID 99 не знайдено.")

        with self.assertRaises(ValueError) as context:
            self.manager.find_order_by_id(-1)
        self.assertEqual(str(context.exception), "ID замовлення має бути цілим числом більше 0.")

    def test_get_all_orders(self):
        self.manager.add_order(1, "Karasiovich", "Iphone", 2)
        self.manager.add_order(2, "Memen", "Iphone", 3)

        with self.assertLogs('root',level='INFO') as log:
            self.manager.get_all_orders()
        self.assertIn("Список усіх замовлень:", log.output[0])

    def test_get_order_count(self):
        self.manager.add_order(1, "Karasiovich", "Iphone", 2)
        self.assertEqual(self.manager.get_order_count(), 1)
        self.manager.add_order(2, "Memen", "Iphone", 3)
        self.assertEqual(self.manager.get_order_count(), 2)

    # Тест, який не пройде: перевірка кількості замовлень після видалення
    def test_remove_order_and_check_count(self):
        self.manager.add_order(1, "Karasiovich", "Iphone", 2)
        self.manager.add_order(2, "Memen", "Iphone", 3)
        self.manager.remove_order_by_id(1)

        # Очікуємо 1 замовлення, але неправильно очікуємо 0
        self.assertEqual(self.manager.get_order_count(), 0, "Кількість замовлень повинна бути 0 після видалення!")

    # Тест, який не пройде: пошук неіснуючого замовлення
    def test_find_nonexistent_order(self):
        with self.assertRaises(ValueError) as context:
            self.manager.find_order_by_id(99)
        # Очікуємо, що помилка буде з іншим повідомленням
        self.assertEqual(str(context.exception), "Замовлення не знайдено!", "Повідомлення має бути неправильним!")

    # Тест, який не пройде: додавання замовлення з негативною кількістю
    def test_add_order_negative_quantity(self):
        with self.assertRaises(ValueError) as context:
            self.manager.add_order(3, "Sidorov", "MacBook", -1)
        self.assertEqual(str(context.exception), "Кількість товару не може бути негативною.", "Повідомлення про помилку не відповідає очікуваному.")

if __name__ == "__main__":
    # Перевірка наявності каталогу для результатів і його створення
    if not os.path.exists('test-reports'):
        os.makedirs('test-reports')

    # Запуск тестів через XMLTestRunner без виклику unittest.main()
    with open('test-reports/test_results.xml', 'wb') as output:
        runner = xmlrunner.XMLTestRunner(output=output)
        unittest.main(testRunner=runner, exit=False)
