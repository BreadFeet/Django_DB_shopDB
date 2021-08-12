class Sql:
    custlistone = "SELECT * FROM cust WHERE id = '%s'";   # Sql문 생각해보면 id = 'id01' 이렇게 따옴표가 들어가야 한다
    custlist = "SELECT * FROM cust";
    custinsert = "INSERT INTO cust VALUES ('%s','%s','%s')";
    custdelete = "DELETE FROM cust WHERE id = '%s'";
    custupdate = "UPDATE cust SET pwd = '%s', name = '%s' WHERE id = '%s'";

    itemlistone = "SELECT * FROM item WHERE id = %d";
    itemlist = "SELECT * FROM item";
    iteminsert = "INSERT INTO item VALUES (NULL, '%s', %d, '%s', CURRENT_DATE())";   # 숫자는 %d는 따옴표 필요 없음
    itemdelete = "DELETE FROM item WHERE id = %d";
    itemupdate = "UPDATE item SET name = '%s', price = %d, imgname = '%s' WHERE id = '%d'";

    cartlist = '''SELECT cu.name, i.name, i.price, ca.num, (i.price * ca.num) as tot_price, i.imgname, ca.regdate
                  FROM cart ca INNER JOIN cust cu ON ca.custid = cu.id 
                               INNER JOIN item i ON ca.itemid = i.id
                  WHERE ca.custid = '%s' '''
    cartinsert = "INSERT INTO cart VALUES (NULL, '%s', %d, %d, CURRENT_DATE())"