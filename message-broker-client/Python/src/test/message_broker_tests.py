import unittest
from io import StringIO
import sys
from datetime import datetime
from unittest.mock import patch

sys.path.append(
    r'C:\Users\mjmah\OneDrive\Desktop\everything\Main\term7\sa\Project\Pycharm\message-broker-client\Python\src\main')
from Consumer import Consumer
from Message import Message
from Producer import Producer


class MessageBrokerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.producer = Producer()
        cls.consumer = Consumer()

    def setUp(self):
        self.outContent = StringIO()
        self.errContent = StringIO()
        sys.stdout = self.outContent
        sys.stderr = self.errContent

    def tearDown(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def test_message_queue_time_guarantee(self):
        message1 = Message("myKey1", "myValue1", datetime.now())
        message2 = Message("myKey2", "myValue2", datetime.now())
        message3 = Message("myKey3", "myValue3", datetime.now())

        # Print the type of object returned by the pull method
        pulled_message = self.consumer.pull()
        print("Type of pulled_message:", type(pulled_message))

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.producer.push(message1)
            self.producer.push(message2)
            self.producer.push(message3)

            self.assertEqual(message1.key, self.consumer.pull().key)
            self.assertEqual(message2.key, self.consumer.pull().key)
            self.assertEqual(message3.key, self.consumer.pull().key)

    def test_subscribe(self):
        message1 = Message("num1", "3", datetime.now())
        message2 = Message("num2", "7", datetime.now())
        message3 = Message("num3", "12", datetime.now())

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.producer.push(message1)
            self.producer.push(message2)
            self.producer.push(message3)

            def calculate_square(message):
                print(int(message.value) ** 2)

            self.consumer.subscribe(calculate_square, 1000)

            self.assertEqual(fake_out.getvalue(), "9\n49\n144\n")

    @classmethod
    def tearDownClass(cls):
        print("successful")


if __name__ == '__main__':
    unittest.main()
