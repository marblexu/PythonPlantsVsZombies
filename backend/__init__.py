# 导入Flask应用和扩展
from .app import app, db
from .models import User, Role, Permission, Log, Resource

# 导入创建初始数据的函数
from .models import create_initial_data