import time
import unittest

import client

squares = set()


def calculate_square(key, value):
    square = int(value) ** 2
    squares.add(square)


class MessageBrokerTests(unittest.TestCase):
    def test_message_queue_time_guarantee(self):
        client.push("key1", "value1")
        client.push("key2", "value2")
        client.push("key3", "value3")

        self.assertEqual(client.pull(), ("key1", "value1"))
        self.assertEqual(client.pull(), ("key2", "value2"))
        self.assertEqual(client.pull(), ("key3", "value3"))

    def test_subscribe(self):
        client.push("num1", "5")
        client.push("num2", "15")
        client.push("num3", "12")
        client.push("num3", "6")

        client.subscribe(calculate_square)

        time.sleep(4)

        expected = {225, 25, 144, 36}

        self.assertEqual(squares, expected)


if __name__ == '__main__':
    unittest.main()
