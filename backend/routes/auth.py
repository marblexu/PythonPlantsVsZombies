from flask import Blueprint, request, jsonify
from backend.app import db
from backend.models import User, Role
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

bp = Blueprint('auth', __name__)

# 配置邮箱
MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-email-password'
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'your-email@gmail.com'

# 创建序列化器
serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY') or 'your-secret-key-here')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'message': 'Username already exists'}), 409
    
    # 检查邮箱是否已存在
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'message': 'Email already exists'}), 409
    
    # 创建新用户
    user = User(
        username=data.get('username'),
        email=data.get('email')
    )
    user.set_password(data.get('password'))
    
    # 赋予默认角色
    default_role = Role.query.filter_by(name='user').first()
    if default_role:
        user.roles.append(default_role)
    
    db.session.add(user)
    db.session.commit()
    
    # 发送验证邮件
    send_verification_email(user)
    
    return jsonify({'message': 'User created successfully. Please check your email to verify your account.'}), 201

@bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = serializer.loads(token, salt='email-verification-salt', max_age=3600)  # 1小时有效期
    except:
        return jsonify({'message': 'Invalid or expired token'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if user.is_verified:
        return jsonify({'message': 'Email already verified'}), 400
    
    user.is_verified = True
    db.session.commit()
    
    return jsonify({'message': 'Email verified successfully'}), 200

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password')):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    if not user.is_verified:
        return jsonify({'message': 'Please verify your email first'}), 403
    
    # 创建访问令牌和刷新令牌
    access_token = user.get_access_token()
    refresh_token = user.get_refresh_token()
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'roles': [role.name for role in user.roles]
        }
    }), 200

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    access_token = user.get_access_token()
    
    return jsonify({'access_token': access_token}), 200

@bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    
    if not data or not data.get('email'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    user = User.query.filter_by(email=data.get('email')).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # 发送重置密码邮件
    send_password_reset_email(user)
    
    return jsonify({'message': 'Password reset email sent. Please check your email.'}), 200

@bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # 1小时有效期
    except:
        return jsonify({'message': 'Invalid or expired token'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    if not data or not data.get('password') or not data.get('confirm_password'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if data.get('password') != data.get('confirm_password'):
        return jsonify({'message': 'Passwords do not match'}), 400
    
    user.set_password(data.get('password'))
    db.session.commit()
    
    return jsonify({'message': 'Password reset successfully'}), 200

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_verified': user.is_verified,
        'roles': [role.name for role in user.roles],
        'created_at': user.created_at,
        'updated_at': user.updated_at
    }), 200

# 发送验证邮件
def send_verification_email(user):
    token = serializer.dumps(user.email, salt='email-verification-salt')
    verification_url = f'http://localhost:5000/api/auth/verify/{token}'
    
    subject = 'Verify your email for Plants vs Zombies'
    body = f'Hi {user.username},\n\nPlease click the link below to verify your email:\n{verification_url}\n\nThis link will expire in 1 hour.\n\nThanks,\nThe Plants vs Zombies Team'
    
    send_email(user.email, subject, body)

# 发送重置密码邮件
def send_password_reset_email(user):
    token = serializer.dumps(user.email, salt='password-reset-salt')
    reset_url = f'http://localhost:5000/api/auth/reset-password/{token}'
    
    subject = 'Reset your password for Plants vs Zombies'
    body = f"Hi {user.username},\n\nYou requested a password reset. Please click the link below to reset your password:\n{reset_url}\n\nThis link will expire in 1 hour.\n\nIf you didn't request this, you can safely ignore this email.\n\nThanks,\nThe Plants vs Zombies Team"
    
    send_email(user.email, subject, body)

# 发送邮件
def send_email(to, subject, body):
    try:
        # 创建邮件消息
        msg = MIMEMultipart()
        msg['From'] = MAIL_DEFAULT_SENDER
        msg['To'] = to
        msg['Subject'] = subject
        
        # 添加邮件正文
        msg.attach(MIMEText(body, 'plain'))
        
        # 连接到SMTP服务器
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        
        # 发送邮件
        server.send_message(msg)
        
        # 关闭连接
        server.quit()
    except Exception as e:
        print(f'Error sending email: {str(e)}')
        # 在这里可以添加日志记录
        pass