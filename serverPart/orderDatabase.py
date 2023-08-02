from enum import Enum

import pymysql


class OrderColumn(Enum):
    orders_id = 0
    big_mac_amount = 1
    french_fries_amount = 2
    big_mac_cost = 3
    french_fries_cost = 4
    total_cost = 5


class OrderDatabase:
    def __init__(self, host=None, user=None, password=None):
        self.host = host or "localhost"
        self.user = user
        self.password = password

        self._conn = None
        self.cur_db_name = "foodorder"
        self.table_name = "orders"
        self._cursor = None
        self.connect_db()
        self.use_ssl = False
        self.ssl = {}

    def connect_db(self):
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.cur_db_name,
        )

        self._cursor = self.conn.cursor()

    def send_order(self, args):
        french_fries_quantity = int(args[0])
        big_mac_quantity = int(args[1])
        french_fries_cost = float(args[2])
        big_mac_cost = float(args[3])
        total_cost = float(args[4])

        cmd = "INSERT INTO  {} \
            (bigmac_amount, french_fries_amount, big_mac_cost, french_fries_cost, total_cost) \
                VALUES(%s, %s, %s, %s, %s)".format(
            self.table_name
        )
        try:
            self._cursor.execute(
                cmd,
                (
                    french_fries_quantity,
                    big_mac_quantity,
                    french_fries_cost,
                    big_mac_cost,
                    total_cost,
                ),
            )
            self.conn.commit()
            return True, None
        except pymysql.Error as e:
            print("Error sending order to the database:", e)
            self.conn.rollback()
            return False, str(e)

    def get_order(self, args):
        order_id = int(args[0])
        cmd = "SELECT * from {} WHERE orders_id=%s".format(self.table_name)
        try:
            self._cursor.execute(cmd, order_id)
            output = self._cursor.fetchone()
            res = dict()
            res["french fries quantity"] = output[OrderColumn.french_fries_amount.value]
            res["big mac quantity"] = output[OrderColumn.big_mac_amount.value]
            res["french fries cost"] = output[OrderColumn.french_fries_cost.value]
            res["big mac cost"] = output[OrderColumn.big_mac_cost.value]
            res["total cost"] = output[OrderColumn.total_cost.value]
            return True, res
        except pymysql.Error as e:
            print("Error getting order to the database:", e)
            self.conn.rollback()
            return False, str(e)
