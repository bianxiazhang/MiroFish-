import requests
import os

# 禁用代理
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'

BASE_URL = "http://localhost:5001"

print("测试健康检查接口...")
session = requests.Session()
session.trust_env = False

r = session.get(f"{BASE_URL}/health")
print(f"状态码: {r.status_code}, 响应: {r.json()}")

print("\n测试注册接口...")
r = session.post(f"{BASE_URL}/api/auth/register", json={"username": "testuser2", "password": "test123456"})
print(f"状态码: {r.status_code}, 响应: {r.text[:200]}")

print("\n测试登录接口...")
r = session.post(f"{BASE_URL}/api/auth/login", json={"username": "testuser", "password": "test123456"})
print(f"状态码: {r.status_code}, 响应: {r.text[:200]}")
