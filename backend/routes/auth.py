from flask import Blueprint, request, jsonify
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.objects(username=data['username']):
        return jsonify({'msg': 'Username already exists'}), 400
    hashed_pw = generate_password_hash(data['password'])
    user = User(username=data['username'], password=hashed_pw).save()
    return jsonify({'msg': 'Registered successfully'})

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.objects(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'msg': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token)

@auth.route('/get_user', methods=['GET'])
def get_user():
    users = User.objects()
    user_list = []
    for user in users:
        user_list.append({
            "id": str(user.id),
            "username": user.username
            # เพิ่ม field อื่นๆ ถ้าต้องการ
        })
    return jsonify(user_list), 200