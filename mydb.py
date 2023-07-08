import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'mypass'
)

cursorObject = dataBase.cursor()

cursorObject.execute('CREATE DATABASE django_employee')

print('Database done')