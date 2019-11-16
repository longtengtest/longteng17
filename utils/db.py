"""
数据库操作, 暂时只支持MySQL,
需要再环境变量中配置DB_URI=mysql://root:password@localhost:3306/test
"""
import os
import re
import pymysql


def parse_db_uri(db_uri):
    """从db_uri中解析出数据host,port,db,user,password等信息，返回字典格式的数据库配置"""
    try:
        db_type, user, password, host, port, db = re.split(r'://|:|@|/', db_uri)
    except ValueError:
        raise ValueError(f'db_uri: {db_uri} - 格式不正确，应为完整的 mysql://root:password@localhost:3306/test 形式')
    if 'mysql' not in db_type:
        raise TypeError('暂时只支持mysql数据库')

    db_conf = dict(host=host, port=int(port), db=db, user=user, password=password)
    return db_conf


class DB(object):
    def __init__(self, db_conf=None):
        if db_conf is None:
            db_url = os.getenv('DB_URI')
            if db_url is None:
                raise ValueError('DB_URL环境变量未配置, 格式为DB_CONF=mysql://root:password@localhost:3306/test')
            db_conf = parse_db_uri(os.getenv('DB_URI'))
        db_conf.setdefault('charset', 'utf8')  # 默认使用utf8编码
        self.conn = pymysql.connect(**db_conf, autocommit=True)  # 使用自动提交
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)  # 使用字典格式的游标

    def query(self, sql):
        """执行sql"""
        print(f'查询sql: {sql}')
        self.cur.execute(sql)
        result = self.cur.fetchall()
        print(f"查询数据: {result}")
        return result

    def change_db(self, sql):
        print(f'执行sql: {sql}')
        self.cur.execute(sql)

    def close(self):
        self.cur.close()
        self.conn.close()


class FuelCardDB(DB):
    def del_card(self, card_number):
        sql = f'DELETE FROM cardinfo WHERE cardNumber="{card_number}"'
        self.change_db(sql)

    def check_card(self, card_number):
        sql = f'SELECT id FROM cardinfo WHERE cardNumber="{card_number}"'
        res = self.query(sql)
        return True if res else False

    def add_card(self, card_number):
        sql = f'INSERT INTO cardinfo (cardNumber) VALUES ({card_number})'
        self.change_db(sql)
