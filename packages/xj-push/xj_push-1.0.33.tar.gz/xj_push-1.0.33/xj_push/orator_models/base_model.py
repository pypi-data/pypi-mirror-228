# encoding: utf-8
"""
@project: djangoModel->__init__
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2023/8/10 8:58
"""
from orator import DatabaseManager

from config.config import JConfig

config = JConfig()
db_config = {
    config.get('main', 'driver', "mysql"): {
        'driver': config.get('main', 'driver', "mysql"),
        'host': config.get('main', 'mysql_host', "127.0.0.1"),
        'database': config.get('main', 'mysql_database', ""),
        'user': config.get('main', 'mysql_user', "root"),
        'password': config.get('main', 'mysql_password', "123456"),
        "port": config.getint('main', 'mysql_port', "3306")
    }
}


base_db = DatabaseManager(db_config)