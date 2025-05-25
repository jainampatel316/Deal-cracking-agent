import requests
import json

def test_webhook():
    webhook_url = "http://localhost:5001/webhook/omnidimension_call_ended"
    payload = {
        "call_id": "test_call_12345",
        "user_email": "testuser@example.com",
        "product_name": "Nike Air Jordan 1 Retro High OG 'Chicago Lost & Found'"
    }
    headers = {"Content-Type": "application/json"}

    print(f"Sending POST request to {webhook_url} with payload: {json.dumps(payload)}")

    try:
        response = requests.post(webhook_url, json=payload, headers=headers, timeout=10) # Added timeout
        print(f"Response Status Code: {response.status_code}")
        try:
            response_json = response.json()
            print(f"Response JSON: {response_json}")
        except json.JSONDecodeError:
            print(f"Response Content (not JSON): {response.text}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: Could not connect to the server at {webhook_url}.")
        print(f"Please ensure 'webhook_server.py' is running.")
    except requests.exceptions.Timeout:
        print(f"Request timed out after 10 seconds.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_webhook()
