from frame.db import Db
from frame.sql import Sql
from frame.value import CartVO


# Item DB 접속
class CartDB(Db):
    def selectCust(self, custid):
        all = []     # CartVO 객체를 모을 리스트
        conn = super().getConnection()
        cursor = conn.cursor()
        cursor.execute(Sql.cartlist %(custid))
        result = cursor.fetchall()
        for i in result:
            cart = CartVO(i[0], i[1], i[2], i[3], i[4], i[5], i[6])
            all.append(cart)
        cursor.close()       # super().close(conn, cursor)와 같음
        conn.close()
        return all

    def insert(self, custid, itemid, num):
        try:
            conn = super().getConnection()
            cursor = conn.cursor()
            cursor.execute(Sql.cartinsert %(custid, itemid, num))
            conn.commit()
        except:
            conn.rollback()
            raise Exception
        finally:
            super().close(conn, cursor)


if __name__ == '__main__':
    # CartDB().insert('id05', 1011, 1)
    result = CartDB().selectCust('id01')
    print(result)



