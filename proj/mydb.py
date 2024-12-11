import mysql.connector

dataBase = mysql.connector.connect(
host = 'localhost',
user = 'root',
passwd = 'root'
)
 
# prepare a cursor object
cursorObject = dataBase.cursor()
# Create a database
cursorObject.execute("CREATE DATABASE g_y_m")
print("Done!")