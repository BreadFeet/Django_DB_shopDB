from frame.db import Db
from frame.sql import Sql
from frame.value import ItemVO

# Item DB 접속
class ItemDB(Db):
    def selectOne(self, id):
        conn = super().getConnection()
        cursor = conn.cursor()
        cursor.execute(Sql.itemlistone %id)   # 출력하면 1
        i = cursor.fetchone()
        # i = cursor. fetchall()     # ((),) 형태로 출력됨
        item = ItemVO(i[0], i[1], i[2], i[3], i[4])
        super().close(conn, cursor)
        return item    # ItemVO 객체

    def selectAll(self):
        all = []
        conn = super().getConnection()
        cursor = conn.cursor()
        cursor.execute(Sql.itemlist)
        result = cursor.fetchall()
        # result = cursor.fetchone()     # 첫번째 ()값 하나만 출력됨
        for i in result:
            item = ItemVO(i[0], i[1], i[2], i[3], i[4])
            all.append(item)
        cursor.close()       # super().close(conn, cursor)와 같음
        conn.close()
        return all           # ItemVO 객체의 list

    def insert(self, name, price, imgname):
        try:
            conn = super().getConnection()
            cursor = conn.cursor()
            cursor.execute(Sql.iteminsert %(name, price, imgname))
            conn.commit()
        except:
            conn.rollback()
            raise Exception
        finally:
            super().close(conn, cursor)

    def delete(self, id):
        try:
            conn = super().getConnection()
            cursor = conn.cursor()
            cursor.execute(Sql.itemdelete %id)
            conn.commit()
        except:
            conn.rollback()
            raise Exception
        finally:
            super().close(conn, cursor)

    def update(self, id, name, price, imgname):
        try:
            conn = super().getConnection()
            cursor = conn.cursor()
            cursor.execute(Sql.itemupdate %(name, price, imgname, id))
            conn.commit()
        except:
            conn.rollback()
            raise Exception
        finally:
            super().close(conn, cursor)

if __name__ == '__main__':
    # result = ItemDB().selectOne(1001)
    # print(result)

    # result = ItemDB().selectAll()   # list로 반환
    # for r in result:
    #     print(r)

    # ItemDB().insert('pants10', 11000, 'pants10.jpg')
    # ItemDB().insert('"pants10"', 11000, '"pants10.jpg"')  # Sql문에서 %s로 따옴표를 하지 않은 경우는 이렇게 따옴표가 삽입되도록 할 수도 있다

    # ItemDB().delete(1004)

    ItemDB().update(1005, 'pants8', 88000, 'pants8.jpg')





