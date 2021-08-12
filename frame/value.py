# Value Object

class CustVO:
    def __init__(self, id, pwd, name):
        self.id = id;
        self.pwd = pwd;
        self.name = name;

    def __str__(self):
        return self.id + ' ' + self.pwd + ' ' + self.name + ' ';  # VO 객체 만들면 출력되는 값


class ItemVO:
    def __init__(self, id, name, price, imgname, regdate):
        self.id = id;
        self.name = name;
        self.price = price;
        self.imgname = imgname;
        self.regdate = regdate;

    def __str__(self):
        return str(self.id) + ' ' + self.name + ' ' \
               + str(self.price) + ' ' + self.imgname + ' ' + str(self.regdate);


class CartVO:
    def __init__(self, custname, itemname, price, num, total, imgname, regdate):
        self.custname = custname
        self.itemname = itemname
        self.price = price
        self.num = num
        self.total = total
        self.imgname = imgname
        self.regdate = regdate

    def __str__(self):
        return self.custname + ' ' + self.itemname \
               + ' ' + str(self.price) + ' ' + str(self.num) + ' ' + str(self.total) \
               + ' ' + self.imgname + ' ' + str(self.regdate)