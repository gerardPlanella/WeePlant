import psycopg2 as pg

#Postgre SQL credentials
SQL_HOST = '188.166.9.142'
SQL_DATABASE = 'wee'
SQL_USERNAME = 'wee'
SQL_PASSWORD = 'weeplant1234'
SQL_PORT = 5432

class DB():

	#__slots__ = ('address')
    
    def __init__(self):
        #Create a connection to the database with our credentials.
        conn = pg.connect(dbname=SQL_DATABASE, user=SQL_USERNAME, password=SQL_PASSWORD, host=SQL_HOST, port=SQL_PORT)
        #Open a cursor to perform database operations
        cur = conn.cursor()
        


