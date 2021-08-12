from frame.db import Db
from frame.error import ErrorCode
from frame.sql import Sql
from frame.value import CustVO

# Customer DB 접속
class CustDB(Db):    # 상위 클래스 Db를 상속받는다
    def selectOne(self, id):
        cust = None    # 최종 출력할 변수 초기화
        conn = super().getConnection()
        cursor = conn.cursor()
        cursor.execute(Sql.custlistone %id)   # 출력하면 데이터 개수(1) 나옴
        c = cursor.fetchone()       # 한 줄을 불러오면 c = ('id01', 'pwd01', '이말숙')
        cust = CustVO(c[0], c[1], c[2])
        super().close(conn, cursor)
        return cust

    def selectAll(self):
        all = []          # 변수 초기화
        conn = super().getConnection()
        cursor = conn.cursor()
        cursor.execute(Sql.custlist)     # 출력하면 4 (db 내 데이터 개수)
        result = cursor.fetchall()      # 테이블의 한 행을 tuple로 담은 것을 모은 tuple
        for c in result:
            cust = CustVO(c[0], c[1], c[2])   # c = ('id01', 'pwd01', '이말숙')
            all.append(cust)
        super().close(conn, cursor)
        return all

    def insert(self, id, pwd, name):
        try:
            conn = super().getConnection()
            cursor = conn.cursor()
            cursor.execute(Sql.custinsert %(id, pwd, name))
            conn.commit()         # 데이터 베이스에 반영
        except:
            conn.rollback()
            raise Exception
        finally:
            super().close(conn, cursor)

    def delete(self, id):
        try:
            conn = super().getConnection()
            cursor = conn.cursor()
            cursor.execute(Sql.custdelete %id)
            conn.commit()
        except:
            conn.rollback()
            raise Exception
        finally:
            super().close(conn, cursor)

    def update(self, id, pwd, name):
        try:
            conn = self.getConnection()    # super() 대신 self 사용 가능
            cursor = conn.cursor()
            cursor.execute(Sql.custupdate %(pwd, name, id))
            conn.commit()    # commit 안하면 저장 안하고 close 하고 나가는 격 -> db에 반영 안됨
        except:
            conn.rollback()
            raise Exception
        finally:
            super().close(conn, cursor)



if __name__ == '__main__':
    result = CustDB().selectOne('id10')
    print(result)

    # result = CustDB().selectAll()
    # for r in result:
    #     print(r)

    # try:
    #     CustDB().insert('id04', 'pwd04', '이말자')
    # except:
    #     print(ErrorCode.e0001)

    # CustDB().delete('id04')

    # CustDB().update('id03', 'pwd03', '이말자')