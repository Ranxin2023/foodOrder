import pymysql


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

        cmd = "INSERT INTO  {} (bigmac_amount, french_fries_amount, big_mac_cost, french_fries_cost, total_cost) VALUES(%s, %s, %s, %s, %s)".format(
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
