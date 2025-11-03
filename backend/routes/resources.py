from flask import Blueprint, request, jsonify, send_from_directory
from backend.app import db
from backend.models import Resource, User
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from werkzeug.utils import secure_filename
from PIL import Image

bp = Blueprint('resources', __name__)

# 配置上传设置
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'uploads')
THUMBNAIL_FOLDER = os.path.join(UPLOAD_FOLDER, 'thumbnails')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'obj', 'fbx', 'glb', 'gltf'}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB

# 创建上传目录
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(THUMBNAIL_FOLDER):
    os.makedirs(THUMBNAIL_FOLDER)

# 检查文件扩展名是否允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 生成缩略图
def generate_thumbnail(image_path, thumbnail_path, size=(150, 150)):
    try:
        with Image.open(image_path) as img:
            img.thumbnail(size)
            img.save(thumbnail_path)
        return True
    except Exception as e:
        print(f'Error generating thumbnail: {str(e)}')
        return False

@bp.route('/resources', methods=['POST'])
@jwt_required()
def upload_resource():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not user.has_permission('resource_upload'):
        return jsonify({'message': 'Permission denied'}), 403
    
    # 检查请求中是否包含文件部分
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    
    # 如果用户没有选择文件，浏览器会提交一个空文件
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    # 检查文件类型
    if not allowed_file(file.filename):
        return jsonify({'message': 'File type not allowed'}), 400
    
    # 获取其他表单数据
    name = request.form.get('name', file.filename.rsplit('.', 1)[0])
    type = request.form.get('type', 'other')
    description = request.form.get('description', '')
    
    # 安全地保存文件名
    filename = secure_filename(file.filename)
    
    # 为每个用户创建单独的目录
    user_upload_folder = os.path.join(UPLOAD_FOLDER, str(current_user_id))
    if not os.path.exists(user_upload_folder):
        os.makedirs(user_upload_folder)
    
    # 保存文件
    file_path = os.path.join(user_upload_folder, filename)
    file.save(file_path)
    
    # 生成缩略图（仅对图片文件）
    thumbnail_path = None
    if filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'bmp'}:
        thumbnail_filename = f'thumbnail_{filename}'
        thumbnail_path = os.path.join(THUMBNAIL_FOLDER, str(current_user_id), thumbnail_filename)
        
        # 为每个用户创建单独的缩略图目录
        user_thumbnail_folder = os.path.join(THUMBNAIL_FOLDER, str(current_user_id))
        if not os.path.exists(user_thumbnail_folder):
            os.makedirs(user_thumbnail_folder)
        
        # 生成缩略图
        generate_thumbnail(file_path, thumbnail_path)
    
    # 创建资源记录
    resource = Resource(
        user_id=current_user_id,
        name=name,
        type=type,
        file_path=file_path,
        thumbnail_path=thumbnail_path,
        description=description
    )
    
    db.session.add(resource)
    db.session.commit()
    
    return jsonify({
        'message': 'Resource uploaded successfully',
        'resource': {
            'id': resource.id,
            'name': resource.name,
            'type': resource.type,
            'description': resource.description,
            'is_active': resource.is_active,
            'created_at': resource.created_at,
            'updated_at': resource.updated_at
        }
    }), 201

@bp.route('/resources', methods=['GET'])
@jwt_required()
def get_resources():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not user.has_permission('resource_read'):
        return jsonify({'message': 'Permission denied'}), 403
    
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    type = request.args.get('type')
    is_active = request.args.get('is_active', type=bool)
    
    # 构建查询
    query = Resource.query.filter_by(user_id=current_user_id)
    
    # 过滤类型
    if type:
        query = query.filter_by(type=type)
    
    # 过滤激活状态
    if is_active is not None:
        query = query.filter_by(is_active=is_active)
    
    # 排序
    if sort_order == 'desc':
        query = query.order_by(getattr(Resource, sort_by).desc())
    else:
        query = query.order_by(getattr(Resource, sort_by).asc())
    
    # 分页
    paginated_resources = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 格式化结果
    resources = []
    for resource in paginated_resources.items:
        resources.append({
            'id': resource.id,
            'name': resource.name,
            'type': resource.type,
            'description': resource.description,
            'is_active': resource.is_active,
            'created_at': resource.created_at,
            'updated_at': resource.updated_at
        })
    
    return jsonify({
        'resources': resources,
        'total': paginated_resources.total,
        'pages': paginated_resources.pages,
        'current_page': paginated_resources.page
    }), 200

@bp.route('/resources/<int:resource_id>', methods=['GET'])
@jwt_required()
def get_resource(resource_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not user.has_permission('resource_read'):
        return jsonify({'message': 'Permission denied'}), 403
    
    resource = Resource.query.filter_by(id=resource_id, user_id=current_user_id).first()
    
    if not resource:
        return jsonify({'message': 'Resource not found'}), 404
    
    return jsonify({
        'id': resource.id,
        'name': resource.name,
        'type': resource.type,
        'description': resource.description,
        'is_active': resource.is_active,
        'created_at': resource.created_at,
        'updated_at': resource.updated_at
    }), 200

@bp.route('/resources/<int:resource_id>', methods=['PUT'])
@jwt_required()
def update_resource(resource_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not user.has_permission('resource_update'):
        return jsonify({'message': 'Permission denied'}), 403
    
    resource = Resource.query.filter_by(id=resource_id, user_id=current_user_id).first()
    
    if not resource:
        return jsonify({'message': 'Resource not found'}), 404
    
    data = request.form
    
    # 更新资源信息
    if data.get('name'):
        resource.name = data.get('name')
    if data.get('type'):
        resource.type = data.get('type')
    if data.get('description') is not None:
        resource.description = data.get('description')
    if data.get('is_active') is not None:
        resource.is_active = data.get('is_active') == 'true' or data.get('is_active') == True
    
    # 检查是否有新文件上传
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '' and allowed_file(file.filename):
            # 删除旧文件
            if os.path.exists(resource.file_path):
                os.remove(resource.file_path)
            
            # 删除旧缩略图
            if resource.thumbnail_path and os.path.exists(resource.thumbnail_path):
                os.remove(resource.thumbnail_path)
            
            # 保存新文件
            filename = secure_filename(file.filename)
            user_upload_folder = os.path.join(UPLOAD_FOLDER, str(current_user_id))
            file_path = os.path.join(user_upload_folder, filename)
            file.save(file_path)
            resource.file_path = file_path
            
            # 生成新的缩略图（仅对图片文件）
            if filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'bmp'}:
                thumbnail_filename = f'thumbnail_{filename}'
                thumbnail_path = os.path.join(THUMBNAIL_FOLDER, str(current_user_id), thumbnail_filename)
                generate_thumbnail(file_path, thumbnail_path)
                resource.thumbnail_path = thumbnail_path
            else:
                resource.thumbnail_path = None
    
    db.session.commit()
    
    return jsonify({
        'message': 'Resource updated successfully',
        'resource': {
            'id': resource.id,
            'name': resource.name,
            'type': resource.type,
            'description': resource.description,
            'is_active': resource.is_active,
            'created_at': resource.created_at,
            'updated_at': resource.updated_at
        }
    }), 200

@bp.route('/resources/<int:resource_id>', methods=['DELETE'])
@jwt_required()
def delete_resource(resource_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not user.has_permission('resource_delete'):
        return jsonify({'message': 'Permission denied'}), 403
    
    resource = Resource.query.filter_by(id=resource_id, user_id=current_user_id).first()
    
    if not resource:
        return jsonify({'message': 'Resource not found'}), 404
    
    # 删除文件
    if os.path.exists(resource.file_path):
        os.remove(resource.file_path)
    
    # 删除缩略图
    if resource.thumbnail_path and os.path.exists(resource.thumbnail_path):
        os.remove(resource.thumbnail_path)
    
    db.session.delete(resource)
    db.session.commit()
    
    return jsonify({'message': 'Resource deleted successfully'}), 200

@bp.route('/resources/<int:resource_id>/download', methods=['GET'])
@jwt_required()
def download_resource(resource_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not user.has_permission('resource_read'):
        return jsonify({'message': 'Permission denied'}), 403
    
    resource = Resource.query.filter_by(id=resource_id, user_id=current_user_id).first()
    
    if not resource:
        return jsonify({'message': 'Resource not found'}), 404
    
    if not os.path.exists(resource.file_path):
        return jsonify({'message': 'File not found'}), 404
    
    return send_from_directory(os.path.dirname(resource.file_path), os.path.basename(resource.file_path), as_attachment=True)