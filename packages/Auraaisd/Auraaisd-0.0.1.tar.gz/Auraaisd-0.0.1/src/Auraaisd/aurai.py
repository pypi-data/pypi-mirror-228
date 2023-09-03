import requests


def auraai(api_key , question):
        # Replace this with your actual API key
        API_KEY = api_key

        # Replace this with the question you want to ask
        question = question

        # URL of your Flask API
        api_url = "https://prepared-sterling-mule.ngrok-free.app/api/v1/chat"  # Update the URL if needed

        # Define the headers with the API key
        headers = {
            "API-Key": API_KEY,
        }

        # Define the query parameters with the question
        params = {
            "question": question,
        }

        # Send a GET request to your Flask API
        response = requests.get(api_url, headers=headers, params=params)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            data = response.json()
            return data['reply']
        else:
            return response.status_code, response.json()
