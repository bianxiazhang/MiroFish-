# MiroFish 登录注册功能使用说明

## 功能概述

已为 MiroFish 项目添加完整的用户认证系统，包括：
- 用户注册功能
- 用户登录功能
- JWT Token 认证
- 路由守卫（未登录用户自动跳转到登录页）
- 登出功能

## 技术栈

### 后端
- **框架**: Flask（不是 FastAPI）
- **数据库**: SQLite（无需安装，轻量级）
- **ORM**: SQLAlchemy
- **密码加密**: passlib + bcrypt
- **Token**: JWT (python-jose)

### 前端
- **框架**: Vue 3 + Vite
- **路由**: Vue Router
- **HTTP客户端**: Axios
- **存储**: localStorage

## 已安装的依赖

### 后端新增依赖
```
sqlalchemy>=2.0.0
passlib[bcrypt]>=1.7.4
python-jose[cryptography]>=3.3.0
```

这些依赖已经通过以下命令安装：
```bash
pip install "passlib[bcrypt]" "python-jose[cryptography]"
pip install sqlalchemy
```

## 文件结构

### 后端新增文件
```
backend/
├── app/
│   ├── models/
│   │   └── user.py          # 用户模型和数据库配置
│   ├── utils/
│   │   └── auth.py          # 认证工具函数（密码加密、JWT生成）
│   ├── api/
│   │   ├── auth.py          # 认证API接口
│   │   └── __init__.py      # 路由注册
│   └── __init__.py          # 应用初始化
└── test_auth.py             # 测试脚本
```

### 前端新增文件
```
frontend/
└── src/
    ├── views/
    │   └── Auth.vue         # 登录/注册页面
    └── router/
        └── index.js         # 路由配置（已更新）
```

## API 接口

### 1. 用户注册
- **接口**: `POST /api/auth/register`
- **请求体**:
```json
{
  "username": "testuser",
  "password": "test123456"
}
```
- **成功响应** (201):
```json
{
  "message": "注册成功",
  "user": {
    "id": 1,
    "username": "testuser"
  }
}
```
- **错误响应** (400):
```json
{
  "error": "用户名已存在"
}
```

### 2. 用户登录
- **接口**: `POST /api/auth/login`
- **请求体**:
```json
{
  "username": "testuser",
  "password": "test123456"
}
```
- **成功响应** (200):
```json
{
  "message": "登录成功",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "testuser"
  }
}
```
- **错误响应** (401):
```json
{
  "error": "用户名或密码错误"
}
```

## 使用步骤

### 1. 启动后端服务
```bash
cd backend
python run.py
```
后端将在 `http://localhost:5001` 启动

### 2. 启动前端服务
```bash
cd frontend
npm run dev
```
前端将在 `http://localhost:5173` 启动

### 3. 访问应用
- 打开浏览器访问 `http://localhost:5173`
- 系统会自动跳转到登录页面 `/auth`
- 点击"注册"按钮，输入用户名和密码（密码至少6个字符）
- 注册成功后，自动切换到登录模式
- 输入用户名和密码登录
- 登录成功后，跳转到主页 `/`

### 4. 测试后端API（可选）
```bash
cd backend
python test_auth.py
```

## 功能特性

### 前端特性
1. **登录/注册切换**: 同一页面支持登录和注册模式切换
2. **表单验证**: 
   - 用户名长度：3-20个字符
   - 密码长度：至少6个字符
   - 注册时需要确认密码
3. **错误提示**: 友好的错误信息显示
4. **路由守卫**: 未登录用户访问受保护页面时自动跳转到登录页
5. **用户信息显示**: 主页显示当前登录用户名
6. **登出功能**: 点击"退出登录"按钮清除本地存储并跳转到登录页

### 后端特性
1. **密码加密**: 使用 bcrypt 加密存储密码
2. **JWT Token**: 登录成功后生成 30 分钟有效期的 Token
3. **数据库自动初始化**: 首次启动时自动创建 users 表
4. **输入验证**: 严格验证用户名和密码格式
5. **错误处理**: 完善的错误处理机制

## 数据库

### SQLite 数据库位置
```
backend/mirofish.db
```

### 数据表结构
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 安全注意事项

1. **生产环境部署前**:
   - 修改 `SECRET_KEY`（在 `backend/app/utils/auth.py` 中）
   - 使用 HTTPS
   - 考虑添加 Token 刷新机制
   - 添加密码强度验证
   - 添加验证码防止暴力破解

2. **当前配置**:
   - Token 有效期：30分钟
   - 密码加密算法：bcrypt
   - 数据库：SQLite（适合开发和小规模部署）

## 常见问题

### Q: 如何重置数据库？
A: 删除 `backend/mirofish.db` 文件，重启后端服务会自动创建新的数据库。

### Q: 如何修改 Token 有效期？
A: 在 `backend/app/utils/auth.py` 中修改 `ACCESS_TOKEN_EXPIRE_MINUTES` 的值。

### Q: 如何添加更多用户字段？
A: 在 `backend/app/models/user.py` 中的 `User` 类添加新字段，然后删除数据库文件重启服务。

### Q: 前端如何获取当前登录用户？
A: 从 `localStorage.getItem('user')` 获取，返回 JSON 字符串，需要用 `JSON.parse()` 解析。

### Q: 如何在 API 请求中携带 Token？
A: 在请求头中添加 `Authorization: Bearer <token>`，或者将 Token 存储在 localStorage 中。

## 下一步建议

1. **增强安全性**:
   - 添加 Token 刷新机制
   - 实现密码重置功能
   - 添加邮箱验证
   - 实现 API 请求签名

2. **用户体验优化**:
   - 添加"记住我"功能
   - 实现密码强度提示
   - 添加用户头像上传
   - 实现用户资料编辑

3. **功能扩展**:
   - 添加角色权限系统
   - 实现第三方登录（GitHub、Google等）
   - 添加用户操作日志
   - 实现用户数据统计

## 总结

登录注册功能已完整实现并集成到 MiroFish 项目中。系统使用 Flask + SQLite + Vue 3 技术栈，提供了安全可靠的用户认证功能。所有代码都遵循项目现有的代码风格和架构模式。
