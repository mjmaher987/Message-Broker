import json
import requests
from datetime import datetime
from Message import Message
from threading import Thread
import time

class Consumer:
    def pull(self):
        message = None
        try:
            # API endpoint
            url = "http://0.0.0.0:8000/pull/"

            # GET request
            response = requests.get(url)

            # Print response code
            print("Response Code:", response.status_code)

            # Parse JSON response
            message_data = json.loads(response.text)
            message = Message(key=message_data["key"], value=message_data["value"], time_arrived=datetime.now())

            # Print the object
            print("Received Object:")
            print("key:", message.key)
            print("value:", message.value)

        except Exception as e:
            print(e)

        return message

    def subscribe(self, function, intervalMillis):
        subscriber_thread = Thread(target=self._subscribe_thread, args=(function, intervalMillis))
        subscriber_thread.start()

    def _subscribe_thread(self, function, intervalMillis):
        while True:
            message = self.pull()
            if message:
                function(message)
            time.sleep(intervalMillis / 1000)

# Example usage
def process_message(message):
    print("Received Message:")
    print("key:", message.key)
    print("value:", message.value)

consumer = Consumer()
consumer.subscribe(process_message, 1000)
