import pymysql
import os
import sys

# mysql -h rds-stack-rdse0e96d00-llfjqw6b4tyo.chms6ayouq5a.eu-west-2.rds.amazonaws.com -P 3306 -u rds_username -p
Database_endpoint = "rds-stack-rdse0e96d00-llfjqw6b4tyo.chms6ayouq5a.eu-west-2.rds.amazonaws.com"
Username = "rds_username"
Password = "9B_pE=PrfmMLbpYxOOe2.lEJ2g=o5,"
# try:
#   print("Connecting to " + Database_endpoint)
#   db = pymysql.connect(host = Database_endpoint, user = Username, password = Password,port=3306)
#   print("Connection successful to " + Database_endpoint)
#   db.close()
# except Exception as e:
#   print("Connection unsuccessful due to " + str(e))


import mysql.connector

mydb = mysql.connector.connect(
  host=Database_endpoint,
  user=Username,
  password=Password
)
print(mydb)