import pymysql


db_connection = pymysql.connect(host="127.0.0.1", user="root", password="FastFinance!77", database="breast_cancer")
print(db_connection.open) #true if connection is successful

cursor = db_connection.cursor() #creates a cursor object, which executes sql commands

ex = cursor.execute("select * from breast_cancer_data where diagnosis = 1;")
print(ex) #should return 357, as that's how many entries have diagnosis = 1 in the db I downloaded

print(cursor.fetchall()) #prints the table as a tuple
