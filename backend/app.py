from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from mongoengine import connect
from config import Config

from routes.auth import auth
from routes.students import students
from routes.medicines import medicines
from routes.treatments import treatments

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
jwt = JWTManager(app)  # เก็บ JWTManager ไว้ในตัวแปร

# เชื่อมต่อ MongoDB ด้วย mongoengine โดยตรง
connect(host=app.config["MONGODB_SETTINGS"]["host"])

# JWT Error Handlers - เพิ่มส่วนนี้
@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return jsonify({'error': 'ต้องมี Authorization token'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    return jsonify({'error': 'Token ไม่ถูกต้อง'}), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token หมดอายุแล้ว'}), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token ถูกยกเลิกแล้ว'}), 401

# ลงทะเบียน Blueprints
app.register_blueprint(auth, url_prefix='/api')
app.register_blueprint(students, url_prefix='/api')
app.register_blueprint(medicines, url_prefix='/api')
app.register_blueprint(treatments, url_prefix='/api')

# Route หลักสำหรับทดสอบ
@app.route('/')
def home():
    return jsonify({'message': 'Hospital API is running!', 'version': '1.0'})

# Route สำหรับดู routes ทั้งหมด (เพื่อ debug)
@app.route('/debug/routes')
def show_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': rule.rule
        })
    return {'routes': routes}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)