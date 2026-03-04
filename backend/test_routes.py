import requests

BASE_URL = "http://localhost:5001"

response = requests.get(f"{BASE_URL}/api/graph")
print(f"状态码: {response.status_code}")
print(f"响应: {response.text}")
