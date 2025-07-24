from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

# MongoDB
connect('nurse_room_db')

# Secret Key สำหรับ JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

# Register Blueprints
from routes.auth import auth
from routes.students import students
from routes.medicines import medicines
from routes.treatments import treatments

app.register_blueprint(auth, url_prefix='/api')
app.register_blueprint(students, url_prefix='/api')
app.register_blueprint(medicines, url_prefix='/api')
app.register_blueprint(treatments, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
