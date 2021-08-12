# mariaDB 연결을 설정함
import pymysql

config = {
    'database': 'shopdb',
    'user': 'shopuser',    # mariaDB에서 사용자 관리자에서 설정한 사용자의 이름/비번
    'password': '0000',
    'host': '127.0.0.1',
    'port': 3306,      # mysql 공통 포트
    'charset': 'utf8',
    'use_unicode': True
}

class Db:
    def getConnection(self):
        conn = pymysql.connect(**config);
        return conn;

    def close(self, conn, cursor):
        if cursor != None:
            cursor.close();
        if conn != None:
            conn.close();