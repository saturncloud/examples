import requests
import json # Import json module

payload = {
    
    "model": "meta-llama/Meta-Llama-3-70B-Instruct", 
    "messages": [
        {"role": "user", "content": "Explain tensor parallelism simply."}
    ]
}

# Use the correct internal address
url = "http://127.0.0.1:8000/v1/chat/completions" 

res = requests.post(url, json=payload)

# Check if the request was successful before parsing JSON
if res.status_code == 200:
    data = res.json()
    print("RAW:", json.dumps(data, indent=2))
    print("\nASSISTANT:", data["choices"][0]["message"]["content"])
else:
    print(f"Request failed with status code {res.status_code}")
    print("Response text:", res.text)
