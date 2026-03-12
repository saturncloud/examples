import requests
import json

def test_prediction(user_id):
    url = "http://localhost:8000/predict"
    payload = {"user_id": user_id}
    headers = {"Content-Type": "application/json"}

    print(f"🚀 Sending request for User ID: {user_id}...")
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"📊 Prediction: {result['prediction']}")
            print(f"🔍 Features Retrieved: {result['features_retrieved']}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    # Test with user IDs we ingested
    test_prediction(101)
    test_prediction(102)