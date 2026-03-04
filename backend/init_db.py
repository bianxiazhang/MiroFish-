from app.models.user import init_db

if __name__ == "__main__":
    print("正在初始化数据库...")
    init_db()
    print("数据库初始化成功！")
    print("数据库文件位置: backend/mirofish.db")
