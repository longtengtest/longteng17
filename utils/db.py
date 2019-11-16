'''数据库操作'''
import pymysql
import os

DB_CONF = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT')),
    'db': os.getenv('MYSQL_DB'),
    'user':  os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PWD'),
    'charset': 'utf8',
    # 'autocommit': True
}
class DB(object):
    def __init__(self, db_conf=DB_CONF):
        self.conn = pymysql.connect(**db_conf, autocommit=True)
        # self.cur = self.conn.cursor()
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)  # 字典游标

    def query(self, sql):
        """执行sql"""
        print(f'查询sql:{sql}')
        self.cur.execute(sql)
        result = self.cur.fetchall()
        print(f"查询数据：{result}")
        return result
    def change_db(self, sql):
        """执行sql"""
        print(f'执行sql:{sql}')
        self.cur.execute(sql)
    def close(self):
        self.cur.close()
        self.conn.close()





if __name__ == '__main__':

    db = DB()
    r = db.query("SELECT * FROM cardinfo WHERE cardNumber='2121452';")
    print(r)
    # db_conf = {
    #     'host': '115.28.',
    #     'port': int(os.getenv('MYSQL_PORT')),
    #     'db': os.getenv('MYSQL_DB'),
    #     'user': os.getenv('MYSQL_USER'),
    #     'password': os.getenv('MYSQL_PWD'),
    #     'charset': 'utf8',
    #     'autocommit': True
    # }