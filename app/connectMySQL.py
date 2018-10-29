import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'root',
  'password': '1q2w3e4r',
  'host': '127.0.0.1',
  'database': 'stock',
  'raise_on_warnings': True
}

DB_NAME = 'stock'

TABLES = {}
TABLES['stock_master'] = (
    "CREATE TABLE `stock_master` ("
    " `stock_id` VARCHAR(10) NOT NULL,"
    " `date` DATE NOT NULL,"
    " `trading_volume` BIGINT NOT NULL,"
    " `turnover_in_value` BIGINT NOT NULL,"
    " `open` FLOAT NULL,"
    " `high` FLOAT NULL,"
    " `low` FLOAT NULL,"
    " `close` FLOAT NULL,"
    " `advance_decline` FLOAT DEFAULT NULL,"
    " `transaction_count` BIGINT NOT NULL,"
    "  PRIMARY KEY (`stock_id`, `date`)"
    ") ENGINE=InnoDB")

TABLES['stock_list'] = (
    "CREATE TABLE `stock_list` ("
    " `stock_id` VARCHAR(10) NOT NULL,"
    "  PRIMARY KEY (`stock_id`, `date`)"
    ") ENGINE=InnoDB")


def getConnection():
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        # cnx.close()
        return cnx

def closeConnection(cnx):
    cursor = cnx.cursor()
    cursor.close()
    cnx.close()


class connect():
    def __init__(self, name):
        self.name = name

    def create_database():
        cnx = mysql.connector.connect(user='root', password='1q2w3e4r', host='127.0.0.1')
        cursor = cnx.cursor()
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        cursor.close()
        cnx.close()


    def create_table():
        cnx = mysql.connector.connect(**config)
        #cnx = getConnection()
        cursor = cnx.cursor()

        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

        cursor.close()
        cnx.close()

    def add_row(add_stock, date_stock):
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        cursor.execute(add_stock, date_stock)
        cnx.commit()

        cursor.close()
        cnx.close()

    def query_row(query):
        cnx = getConnection()
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        closeConnection(cnx)
        return result