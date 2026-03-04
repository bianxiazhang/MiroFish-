import requests
import json

BASE_URL = "http://127.0.0.1:5001"

print("使用 127.0.0.1 测试...")

print("\n1. 测试健康检查...")
r = requests.get(f"{BASE_URL}/health")
print(f"状态码: {r.status_code}")

print("\n2. 测试登录...")
headers = {'Content-Type': 'application/json'}
r = requests.post(f"{BASE_URL}/api/auth/login", 
                  data=json.dumps({"username": "testuser", "password": "test123456"}),
                  headers=headers)
print(f"状态码: {r.status_code}")
print(f"响应: {r.text[:300]}")
