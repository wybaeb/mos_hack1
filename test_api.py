import requests

# Define the API token and the base URL
API_TOKEN = "your_secure_token"
BASE_URL = "http://127.0.0.1:5001"

# Define the headers for the request
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Define the test payload
payload = {
    "text": "testКак погодка сегодня?"
}

# Send a POST request to the API endpoint
response = requests.post(f"{BASE_URL}/interact", json=payload, headers=headers)

# Print the response from the API
print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except ValueError:
    print("Response content:", response.text)
