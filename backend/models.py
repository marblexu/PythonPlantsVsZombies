from datetime import datetime
from .app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

# 用户角色关联表
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

# 角色权限关联表
roles_permissions = db.Table('roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联角色
    roles = db.relationship('Role', secondary=roles_users, lazy='subquery',
        backref=db.backref('users', lazy=True))
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_access_token(self):
        return create_access_token(identity=self.id)
    
    def get_refresh_token(self):
        return create_refresh_token(identity=self.id)
    
    def has_permission(self, permission_name):
        for role in self.roles:
            for permission in role.permissions:
                if permission.name == permission_name:
                    return True
        return False

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联权限
    permissions = db.relationship('Permission', secondary=roles_permissions, lazy='subquery',
        backref=db.backref('roles', lazy=True))
    
    def __repr__(self):
        return f'<Role {self.name}>'

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Permission {self.name}>'

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(255))
    importance = db.Column(db.Integer, default=1)  # 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联用户
    user = db.relationship('User', backref=db.backref('logs', lazy=True))
    
    def __repr__(self):
        return f'<Log {self.title}>'

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # skin, model, etc.
    file_path = db.Column(db.String(255), nullable=False)
    thumbnail_path = db.Column(db.String(255))
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联用户
    user = db.relationship('User', backref=db.backref('resources', lazy=True))
    
    def __repr__(self):
        return f'<Resource {self.name}>'

# 创建初始数据
def create_initial_data():
    # 创建权限
    permissions = [
        ('log_create', 'Create log'),
        ('log_read', 'Read log'),
        ('log_update', 'Update log'),
        ('log_delete', 'Delete log'),
        ('resource_upload', 'Upload resource'),
        ('resource_read', 'Read resource'),
        ('resource_update', 'Update resource'),
        ('resource_delete', 'Delete resource'),
        ('user_manage', 'Manage user'),
        ('role_manage', 'Manage role'),
    ]
    
    for name, description in permissions:
        permission = Permission.query.filter_by(name=name).first()
        if not permission:
            permission = Permission(name=name, description=description)
            db.session.add(permission)
    
    # 创建角色
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='Administrator role')
        # 赋予所有权限
        admin_role.permissions = Permission.query.all()
        db.session.add(admin_role)
    
    user_role = Role.query.filter_by(name='user').first()
    if not user_role:
        user_role = Role(name='user', description='Regular user role')
        # 赋予基本权限
        user_role.permissions = Permission.query.filter_by(name.in_([
            'log_create', 'log_read', 'log_update', 'log_delete',
            'resource_upload', 'resource_read', 'resource_update', 'resource_delete'
        ])).all()
        db.session.add(user_role)
    
    # 创建管理员用户
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(username='admin', email='admin@example.com', is_verified=True)
        admin_user.set_password('admin123')
        admin_user.roles.append(admin_role)
        db.session.add(admin_user)
    
    db.session.commit()