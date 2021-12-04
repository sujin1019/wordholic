import pymysql
from controllers.db_controller import mysql_access_info

MYSQL_CONN = pymysql.connect(
    host=mysql_access_info()['host'], 
    port=3306, 
    user=mysql_access_info()['user'],
    passwd=mysql_access_info()['passwd'],
    db=mysql_access_info()['db'], 
    charset='utf8')


def conn_mysql():
    if not MYSQL_CONN.open:
        MYSQL_CONN.ping(reconnect=True)
    return MYSQL_CONN