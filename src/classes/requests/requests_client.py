import requests


class RequestsClient:
    def __init__(self):
        pass

    def send_request(self, method, url, headers=None, data=None):
        try:
            if method == "GET":
                response = requests.get(url=url, headers=headers, data=data)
            elif method == "POST":
                response = requests.post(url=url, headers=headers, data=data)
            else:
                raise ValueError(f"Unsupported request method: {method}")

            if response.status_code == 200:
                return response.json()
            else:
                return response.text

        except requests.RequestException as e:
            # If an error occurs during the request, print the error message
            print(f"An error occurred: {e}")
