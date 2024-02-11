import json
import requests

class Consumer:
    def pull(self):
        message = None
        try:
            # API endpoint
            url = "https://jsonplaceholder.typicode.com/posts/1"

            # GET request
            response = requests.get(url)

            # Print response code
            print("Response Code:", response.status_code)

            # Parse JSON response
            message = json.loads(response.text)

            # Print the object
            print("Received Object:")
            print("key:", message["key"])
            print("value:", message["value"])

        except Exception as e:
            print(e)

        return message

# Example usage
consumer = Consumer()
consumer.pull()
