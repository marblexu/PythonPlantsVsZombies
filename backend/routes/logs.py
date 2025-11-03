from flask import Blueprint, request, jsonify
from backend.app import db
from backend.models import Log, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

bp = Blueprint('logs', __name__)

@bp.route('/logs', methods=['POST'])
@jwt_required()
def create_log():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not user.has_permission('log_create'):
        return jsonify({'message': 'Permission denied'}), 403
    
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # 创建新日志
    log = Log(
        user_id=current_user_id,
        title=data.get('title'),
        content=data.get('content'),
        tags=data.get('tags'),
        importance=data.get('importance', 1)
    )
    
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'message': 'Log created successfully',
        'log': {
            'id': log.id,
            'title': log.title,
            'content': log.content,
            'tags': log.tags,
            'importance': log.importance,
            'created_at': log.created_at,
            'updated_at': log.updated_at
        }
    }), 201

@bp.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not user.has_permission('log_read'):
        return jsonify({'message': 'Permission denied'}), 403
    
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    tags = request.args.get('tags')
    importance = request.args.get('importance', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # 构建查询
    query = Log.query.filter_by(user_id=current_user_id)
    
    # 过滤标签
    if tags:
        tag_list = tags.split(',')
        for tag in tag_list:
            query = query.filter(Log.tags.like(f'%{tag}%'))
    
    # 过滤重要程度
    if importance:
        query = query.filter_by(importance=importance)
    
    # 过滤日期范围
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Log.created_at >= start)
        except ValueError:
            return jsonify({'message': 'Invalid start date format. Use YYYY-MM-DD'}), 400
    
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Log.created_at <= end)
        except ValueError:
            return jsonify({'message': 'Invalid end date format. Use YYYY-MM-DD'}), 400
    
    # 排序
    if sort_order == 'desc':
        query = query.order_by(getattr(Log, sort_by).desc())
    else:
        query = query.order_by(getattr(Log, sort_by).asc())
    
    # 分页
    paginated_logs = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 格式化结果
    logs = []
    for log in paginated_logs.items:
        logs.append({
            'id': log.id,
            'title': log.title,
            'content': log.content,
            'tags': log.tags,
            'importance': log.importance,
            'created_at': log.created_at,
            'updated_at': log.updated_at
        })
    
    return jsonify({
        'logs': logs,
        'total': paginated_logs.total,
        'pages': paginated_logs.pages,
        'current_page': paginated_logs.page
    }), 200

@bp.route('/logs/<int:log_id>', methods=['GET'])
@jwt_required()
def get_log(log_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not user.has_permission('log_read'):
        return jsonify({'message': 'Permission denied'}), 403
    
    log = Log.query.filter_by(id=log_id, user_id=current_user_id).first()
    
    if not log:
        return jsonify({'message': 'Log not found'}), 404
    
    return jsonify({
        'id': log.id,
        'title': log.title,
        'content': log.content,
        'tags': log.tags,
        'importance': log.importance,
        'created_at': log.created_at,
        'updated_at': log.updated_at
    }), 200

@bp.route('/logs/<int:log_id>', methods=['PUT'])
@jwt_required()
def update_log(log_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not user.has_permission('log_update'):
        return jsonify({'message': 'Permission denied'}), 403
    
    log = Log.query.filter_by(id=log_id, user_id=current_user_id).first()
    
    if not log:
        return jsonify({'message': 'Log not found'}), 404
    
    data = request.get_json()
    
    # 更新日志信息
    if data.get('title'):
        log.title = data.get('title')
    if data.get('content'):
        log.content = data.get('content')
    if data.get('tags') is not None:
        log.tags = data.get('tags')
    if data.get('importance') is not None:
        log.importance = data.get('importance')
    
    db.session.commit()
    
    return jsonify({
        'message': 'Log updated successfully',
        'log': {
            'id': log.id,
            'title': log.title,
            'content': log.content,
            'tags': log.tags,
            'importance': log.importance,
            'created_at': log.created_at,
            'updated_at': log.updated_at
        }
    }), 200

@bp.route('/logs/<int:log_id>', methods=['DELETE'])
@jwt_required()
def delete_log(log_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not user.has_permission('log_delete'):
        return jsonify({'message': 'Permission denied'}), 403
    
    log = Log.query.filter_by(id=log_id, user_id=current_user_id).first()
    
    if not log:
        return jsonify({'message': 'Log not found'}), 404
    
    db.session.delete(log)
    db.session.commit()
    
    return jsonify({'message': 'Log deleted successfully'}), 200