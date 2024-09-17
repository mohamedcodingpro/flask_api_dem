import requests
import hmac
import hashlib
import base64
import json
import time

# Replace with your actual API key and secret
API_KEY = 'AIzaSyD4XgKCysD-FngDe-lzonfrTeStOwodsgU'  # Use your Gemini API key here
API_SECRET = 'AIzaSyD4XgKCysD-FngDe-lzonfrTeStOwodsgU'  # Use your Gemini API secret here

# Updated Gemini API endpoint
url = "https://api.gemini.com/v1/balances"

# Create a payload for the request
nonce = str(int(time.time() * 1000))  # A unique number for each request
payload = {
    "request": "/v1/balances",
    "nonce": nonce
}

# Encode the payload and generate the signature
encoded_payload = base64.b64encode(json.dumps(payload).encode())
signature = hmac.new(API_SECRET.encode(), encoded_payload, hashlib.sha384).hexdigest()

# Set up request headers
headers = {
    'Content-Type': 'text/plain',
    'X-GEMINI-APIKEY': API_KEY,
    'X-GEMINI-PAYLOAD': encoded_payload.decode(),
    'X-GEMINI-SIGNATURE': signature,
}

# Send the POST request to the API endpoint
try:
    response = requests.post(url, headers=headers)

    # Check if the response status is successful
    if response.status_code == 200:
        balance_data = response.json()
        print("Balance Information:", balance_data)  # Display the balance information

        # Save balance data to a JSON file
        with open("gemini_balances.json", "w") as file:
            json.dump(balance_data, file)
        print("JSON file 'gemini_balances.json' has been created.")

    else:
        print(f"Error {response.status_code}: {response.text}")  # Display error message
except Exception as e:
    print(f"An error occurred: {e}")
