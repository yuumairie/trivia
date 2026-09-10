# Use PyMySQL as a pure-Python stand-in for MySQLdb when DB_ENGINE=mysql,
# so the mysql backend works without compiling mysqlclient.
import pymysql

pymysql.install_as_MySQLdb()
