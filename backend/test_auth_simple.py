import requests
import json

BASE_URL = "http://localhost:5001"

def test_register():
    print("=" * 50)
    print("测试注册接口")
    print("=" * 50)
    
    url = f"{BASE_URL}/api/auth/register"
    data = {
        "username": "testuser",
        "password": "test123456"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 201
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_login():
    print("\n" + "=" * 50)
    print("测试登录接口")
    print("=" * 50)
    
    url = f"{BASE_URL}/api/auth/login"
    data = {
        "username": "testuser",
        "password": "test123456"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

if __name__ == "__main__":
    print("MiroFish 认证系统测试")
    print("请确保后端服务已启动在 http://localhost:5001\n")
    
    register_success = test_register()
    login_success = test_login()
    
    print("\n" + "=" * 50)
    print("测试结果")
    print("=" * 50)
    print(f"注册测试: {'✓ 通过' if register_success else '✗ 失败'}")
    print(f"登录测试: {'✓ 通过' if login_success else '✗ 失败'}")
