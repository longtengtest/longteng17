"""数据库操作"""
import pymysql
import os


DB_CONF = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT')),
    'db': os.getenv('MYSQL_DB'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PWD'),
    'charset': 'utf8',
}


class DB(object):
    def __init__(self, db_conf=DB_CONF):
        self.conn = pymysql.connect(**db_conf, autocommit=True)
        # self.cur = self.conn.cursor()
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)

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


if __name__ == '__main__':
    db = DB()
    r = db.query('SELECT * FROM cardinfo WHERE cardNumber=2121452;')
    print(r)

    db_conf2 = {
        'host': '115.28.108.130',
        'port': 3306,
        'db': 'api_test',
        'user': 'test',
        'password': 'abc123456',
        'charset': 'utf8'
    }

    db2 = DB(db_conf2)
    db2.query('select * from user where name="张三"')

