from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 配置应用
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 配置JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or 'your-jwt-secret-key-here'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1小时
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 604800  # 7天

# 初始化扩展
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# 导入模型
from .models import User, Role, Permission, Log, Resource

# 导入路由
from .routes import auth, logs, resources

# 注册蓝图
app.register_blueprint(auth.bp, url_prefix='/api/auth')
app.register_blueprint(logs.bp, url_prefix='/api/logs')
app.register_blueprint(resources.bp, url_prefix='/api/resources')

# 根路由
@app.route('/')
def index():
    return jsonify({'message': 'Welcome to Plants vs Zombies API'})

if __name__ == '__main__':
    app.run(debug=True)