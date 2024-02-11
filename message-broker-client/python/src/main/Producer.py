import json
import requests

class Producer:
    def push(self, message):
        try:
            # Convert Message to JSON
            json_body = json.dumps(message.__dict__)

            # Define the API endpoint
            url = "https://jsonplaceholder.typicode.com/posts"

            # Set up the request
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            # POST request
            response = requests.post(url, data=json_body, headers=headers)

            # Print response code
            print("Response Code:", response.status_code)

            # Print response body
            print("Response Body:")
            print(response.text)

        except Exception as e:
            print(e)

# Example usage
# producer = Producer()
# message = Message(key="example", value="test", time_arrived=datetime.now())
# producer.push(message)
