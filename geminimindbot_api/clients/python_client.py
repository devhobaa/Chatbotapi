import os
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000/chat")
API_KEY = os.getenv("SERVICE_API_KEY", "change-me")

payload = {"message": "hello from client", "history": []}
headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

r = requests.post(API_URL, json=payload, headers=headers, timeout=60)
print(r.status_code, r.json())
