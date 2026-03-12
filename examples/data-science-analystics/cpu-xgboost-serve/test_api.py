import requests

url = "http://127.0.0.1:8000/predict"

# Profile: 1st Class, Female (1), Age 22, 0 siblings, 0 parents, Fare 71.0
passenger_1 = [1, 1, 22, 0, 0, 71.0]

print(f"🚀 Predicting Survival for Passenger...")
response = requests.post(url, json={"features": passenger_1})
result = response.json()

print("\n--- Prediction Reply ---")
print(f"Outcome:     {result['result']}")
print(f"Confidence:  {result['probability']}")