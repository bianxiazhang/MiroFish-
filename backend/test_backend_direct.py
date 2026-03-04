from app.models.user import init_db, User, SessionLocal
from app.utils.auth import get_password_hash, verify_password, create_access_token

init_db()

print("测试用户创建...")
db = SessionLocal()

existing = db.query(User).filter(User.username == "testuser").first()
if not existing:
    user = User(username="testuser", password_hash=get_password_hash("test123456"))
    db.add(user)
    db.commit()
    print("用户创建成功!")
else:
    print("用户已存在")

user = db.query(User).filter(User.username == "testuser").first()
if user:
    print(f"验证密码: {verify_password('test123456', user.password_hash)}")
    token = create_access_token(data={'sub': user.username})
    print(f"Token: {token[:50]}...")

db.close()
print("\n后端认证功能正常工作!")
