from flask import Blueprint, request, jsonify
from app.models.user import User, get_db
from app.utils.auth import get_password_hash, verify_password, create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    if len(username) < 3 or len(username) > 20:
        return jsonify({'error': '用户名长度必须在3-20个字符之间'}), 400
    
    if len(password) < 6:
        return jsonify({'error': '密码长度不能少于6个字符'}), 400
    
    db = next(get_db())
    
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return jsonify({'error': '用户名已存在'}), 400
    
    password_hash = get_password_hash(password)
    new_user = User(username=username, password_hash=password_hash)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return jsonify({
        'message': '注册成功',
        'user': {
            'id': new_user.id,
            'username': new_user.username
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    db = next(get_db())
    
    user = db.query(User).filter(User.username == username).first()
    
    if not user or not verify_password(password, user.password_hash):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    access_token = create_access_token(data={'sub': user.username})
    
    return jsonify({
        'message': '登录成功',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username
        }
    }), 200
