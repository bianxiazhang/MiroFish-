import requests

BASE_URL = "http://localhost:5001"

print("测试健康检查接口...")
r = requests.get(f"{BASE_URL}/health")
print(f"状态码: {r.status_code}, 响应: {r.json()}")

print("\n测试注册接口...")
r = requests.post(f"{BASE_URL}/api/auth/register", json={"username": "testuser", "password": "test123456"})
print(f"状态码: {r.status_code}, 响应: {r.text[:200]}")

print("\n测试登录接口...")
r = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "testuser", "password": "test123456"})
print(f"状态码: {r.status_code}, 响应: {r.text[:200]}")
