#!/usr/bin/python
import psycopg2 as pg
import random

#Postgre SQL credentials
SQL_HOST = '188.166.9.142'
SQL_DATABASE = 'wee'
SQL_USERNAME = 'wee'
SQL_PASSWORD = 'weeplant1234'
SQL_PORT = 5432

class WeePlantDB():
    def __init__(self):
        #Create a connection to the database with our credentials.
        self.conn = pg.connect(dbname=SQL_DATABASE, user=SQL_USERNAME, password=SQL_PASSWORD, host=SQL_HOST, port=SQL_PORT, sslmode="prefer")

    def closeDB(self):
        self.conn.close()

    def resetTables(self):
        cursor = self.conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS Plant CASCADE;', vars=None)
        cursor.execute("""CREATE TABLE Plant (
                            plant_ID SERIAL,
                            name VARCHAR(255),
                            pot_number SMALLINT,
                            watering_time NUMERIC,
                            moisture_threshold NUMERIC,
                            photo_period INT,
                            PRIMARY KEY (plant_ID));""", vars=None)

        cursor.execute('DROP TABLE IF EXISTS Imatge CASCADE;', vars=None)
        cursor.execute("""CREATE TABLE Imatge (
                            time TIMESTAMP,
                            plant_ID INT,
                            image BYTEA,
                            height REAL,
                            colour SMALLINT[],
                            PRIMARY KEY (time, plant_ID),
                            FOREIGN KEY (plant_ID) REFERENCES Plant(plant_ID) );""", vars=None)

        cursor.execute('DROP TABLE IF EXISTS Humidity CASCADE;', vars=None)
        cursor.execute("""CREATE TABLE Humidity (
                            time TIMESTAMP,
                            plant_ID INT,
                            value REAL,
                            PRIMARY KEY (time, plant_ID),
                            FOREIGN KEY (plant_ID) REFERENCES Plant(plant_ID));""", vars=None)
        self.conn.commit()
        cursor.close()

    def addTestData(self):
        cursor = self.conn.cursor()

        queryPlants = "INSERT INTO Plant(name, pot_number, watering_time, moisture_threshold, photo_period) VALUES "
        queryPlants += "('Rafflesia arnoldii', 1, 500, .7, 200),"
        queryPlants += "('Dracaena cinnabari', 2, 10, .2, 20),"
        queryPlants += "('Tacca chantrieri', 3, 1, .9, 2);"
        cursor.execute(queryPlants)

        from PIL import Image
        image1 = open('images/1.jpg', 'rb').read()
        image2 = open('images/2.jpeg', 'rb').read()
        image3 = open('images/3.jpg', 'rb').read()

        bi1 = pg.Binary(image1)
        bi2 = pg.Binary(image2)
        bi3 = pg.Binary(image3)

        queryImages = "INSERT INTO Imatge(time, plant_ID, image, height, colour) VALUES "
        queryImages += "('1999-01-08 04:05:06', 1, %s, 35, ARRAY[255, 0, 0]),"
        queryImages += "('1999-01-08 04:05:06', 2, %s, 400, ARRAY[10, 255, 0]),"
        queryImages += "('1999-01-08 04:05:06', 3, %s, 5, ARRAY[2, 200, 200]);"
        cursor.execute(queryImages, (bi1, bi2, bi3, ))

        queryHumidity = "INSERT INTO Humidity(time, plant_ID, value) VALUES "
        queryHumidity += "('1999-01-08 04:05:06', 1, .4),"

        for j in range (3):
            for i in range(100):
                hum = random.randint(((10*(j+1))+10), (100 - 10*(j+1))) / 100
                queryHumidity += "(\'1999-01-08 04:" + str(int(i/60)) + ":" + str(int(i%60)) + "\', " + str(j+1) + ", " + str(hum) + "), "
        queryHumidity = queryHumidity[:-2] + ";"
        cursor.execute(queryHumidity, vars=None)
        self.conn.commit()
        cursor.close()

    def printTable(self, name):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM ' + name + ';', vars=None)

        for row in cursor:
            print(list(row))
        cursor.close()

    def getPlant(self, id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM plant WHERE plant_ID = %s;', (str(id),))

        resultat = {}
        for row in cursor:
            resultat = {
                "plant_ID": row[0],
                "name": row[1],
                "pot_number": row[2],
                "watering_time": row[3],
                "moisture_threshold": row[4],
                "photo_period": row[5]
                }

        cursor.close()
        return resultat

    def getHumidityLog(self, id):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT h.time, h.plant_ID, h.value
                            FROM humidity h
                            INNER JOIN plant p ON p.plant_ID = h.plant_ID
                            WHERE h.plant_ID = %s
                            ORDER BY time ASC;""", (str(id), ))

        resultat = []
        for row in cursor:
            mostra = {
                "time": row[0],
                "plant_ID": row[1],
                "value": row[2]
                }
            resultat.append(mostra)

        cursor.close()
        return resultat

    def getHumidityLast(self, id):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT h.time, h.plant_ID, h.value
                            FROM humidity h
                            INNER JOIN plant p ON p.plant_ID = h.plant_ID
                            WHERE h.plant_ID = %s
                            ORDER BY time DESC
                            LIMIT 1;""", (str(id), ))

        resultat = {}
        for row in cursor:
            resultat = {
                "time": row[0],
                "plant_ID": row[1],
                "value": row[2]
                }

        cursor.close()
        return resultat

    def addHumidityMeasure(self, time, plant_id, value):
        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO Humidity (time, plant_ID, value)
                            VALUES (%s, %s, %s)""",
                            (str(time), str(plant_id), str(value),))
        self.conn.commit()
        cursor.close()

    def getImages(self, plant_id):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT image
                            FROM imatge
                            WHERE plant_ID = %s
                            ORDER BY time;""", (str(plant_id), ))

        resultat = []
        for row in cursor:
            print(row)
            resultat.append(row[0])

        cursor.close()
        return resultat

    def getImages(self, plant_id):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT image
                            FROM imatge
                            WHERE plant_ID = %s
                            ORDER BY time;""", (str(plant_id), ))

        resultat = []
        i = 0
        for row in cursor:
            resultat.append(row[0])
            #open(str(plant_id) + "_" + str(i) + ".jpg", 'wb').write(row[0])
            i += 1

        cursor.close()
        return resultat

    def addImage(self, time, plant_id, image, height, colour):
        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO Imatge (time, plant_ID, image, height, colour) VALUES
                            (%s, %s, %s, %s, ARRAY%s)""",
                            (str(time), str(plant_id), pg.Binary(image), str(height), str(colour))))
        self.conn.commit()
        cursor.close()

db = WeePlantDB()
#db.printTable("imatge")

#print(db.getHumidityLog(2))

#db.resetTables()
#db.addTestData()

#db.getImages(3)
#print(db.getPlant(1))
#db.printTable('humidity')
db.closeDB()
