import json
import requests
from Message import Message


class Producer:
    PUSH_URL = "http://0.0.0.0:8000/push/"

    def push(self, message):
        try:
            json_body = json.dumps(message.__dict__)

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            response = requests.post(self.PUSH_URL, data=json_body, headers=headers)

            print("Response Code:", response.status_code)

        except Exception as e:
            print(e)
