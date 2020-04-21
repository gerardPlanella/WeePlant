#!/usr/bin/python
import psycopg2 as pg
import random
import operator as op
import base64
from PIL import Image

"""
Funcions de la classe:
 - closeDB()

 - resetTables()
 - addTestData()
 - printTable()

 - getPlant()
 - addPlant()

 - getHumidityLog()
 - getHumidityLast()
 - addHumidityMeasure()
 - getImages()
 - addImage()
"""

#Postgre SQL credentials
SQL_HOST = '188.166.9.142'
SQL_DATABASE = 'wee'
SQL_USERNAME = 'wee'
SQL_PASSWORD = 'weeplant1234'
SQL_PORT = 5432

# Classe que permet interactuar amb la base de dades al servidor remot
class WeePlantDB():
    def __init__(self):
        #Create a connection to the database with our credentials.
        self.conn = pg.connect(dbname=SQL_DATABASE, user=SQL_USERNAME, password=SQL_PASSWORD, host=SQL_HOST, port=SQL_PORT, sslmode="prefer")

    #Funció per a aliberar els recursos i tancar la connexió amb la DB
    def closeDB(self):
        self.conn.close()

    #Elimina tot el contingut de les taules de la base de dades i les torna a generar
    def resetTables(self):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()

        #Borrem la taula Plant
        cursor.execute('DROP TABLE IF EXISTS Plant CASCADE;', vars=None)
        #Tornem a crear la taula Plant (buida)
        cursor.execute("""CREATE TABLE Plant (
                            plant_ID SERIAL,
                            name VARCHAR(255),
                            pot_number SMALLINT,
                            since DATE,
                            watering_time NUMERIC,
                            moisture_threshold NUMERIC,
                            moisture_period INT,
                            photo_period INT,
                            PRIMARY KEY (plant_ID));""", vars=None)

        #Borrem la taula Imatge
        cursor.execute('DROP TABLE IF EXISTS Imatge CASCADE;', vars=None)
        #Tornem a crear la taula Imatge (buida)
        cursor.execute("""CREATE TABLE Imatge (
                            time TIMESTAMP,
                            plant_ID INT,
                            image text,
                            height REAL,
                            colour NUMERIC[][],
                            PRIMARY KEY (time, plant_ID),
                            FOREIGN KEY (plant_ID) REFERENCES Plant(plant_ID) );""", vars=None)

        #Borrem la taula Humidity
        cursor.execute('DROP TABLE IF EXISTS Humidity CASCADE;', vars=None)
        #Tornem a crear la taula Humidity (buida)
        cursor.execute("""CREATE TABLE Humidity (
                            time TIMESTAMP,
                            plant_ID INT,
                            value REAL,
                            PRIMARY KEY (time, plant_ID),
                            FOREIGN KEY (plant_ID) REFERENCES Plant(plant_ID));""", vars=None)

        #Borrem la taula Humidity
        cursor.execute('DROP TABLE IF EXISTS Watering CASCADE;', vars=None)
        #Tornem a crear la taula Humidity (buida)
        cursor.execute("""CREATE TABLE Watering (
                            time TIMESTAMP,
                            plant_ID INT,
                            water_applied REAL,
                            PRIMARY KEY (time, plant_ID),
                            FOREIGN KEY (plant_ID) REFERENCES Plant(plant_ID));""", vars=None)

        #Afegim els canvis realitzats a la base de dades real
        self.conn.commit()
        #Tanquem l'objecte
        cursor.close()

    #Afegeix un conjunt de informació falsa per finalitats de testing del sistema
    def addTestData(self):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()

        # Creem i executem la query per carregar les plantes de prova
        queryPlants = "INSERT INTO Plant(name, pot_number, since, watering_time, moisture_threshold, moisture_period, photo_period) VALUES "
        queryPlants += "('Rafflesia arnoldii', 1, '1999-01-08 04:05:06', 500, .7, 300, 200), "
        queryPlants += "('Dracaena cinnabari', 2, '1999-01-08 04:05:06', 10, .2, 600, 40), "
        queryPlants += "('Tacca chantrieri', 3, '1999-01-08 04:05:06', 1, .9, 60, 20);"
        cursor.execute(queryPlants)

        # Preparem i executem la query per carregar les imatges
        # Obrim les imatges
        image1 = open('images/1.jpg', 'rb').read()
        image2 = open('images/2.jpeg', 'rb').read()
        image3 = open('images/3.jpg', 'rb').read()

        color1 = []
        color2 = []
        color3 = []
        for j in range (3):
            color1.append([])
            color2.append([])
            color3.append([])
            for i in range(255):
                color1[j].append(i % 255)
                color2[j].append((255 - i) % 255)
                color3[j].append(int((255*(i+.1)**(-1))%255))

        # Preparem i executem la query
        queryImages = "INSERT INTO Imatge(time, plant_ID, image, height, colour) VALUES "
        queryImages += "('1999-01-08 04:05:06', 1, %s, 35, %s),"
        queryImages += "('1999-01-09 04:05:06', 1, %s, 35, %s),"
        queryImages += "('1999-01-10 04:05:06', 1, %s, 35, %s),"
        queryImages += "('1999-01-08 04:05:06', 2, %s, 400, %s),"
        queryImages += "('1999-01-08 04:05:06', 3, %s, 5, %s);"
        
        cursor.execute(queryImages,(str(base64.b64encode(image1))[2:-1], color1,
                                    str(base64.b64encode(image2))[2:-1], color2,
                                    str(base64.b64encode(image3))[2:-1], color3,
                                    str(base64.b64encode(image2))[2:-1], color3,
                                    str(base64.b64encode(image3))[2:-1], color2, ))

        # Query per a carregar informació de un log d'humitat
        queryHumidity = "INSERT INTO Humidity(time, plant_ID, value) VALUES "
        queryHumidity += "('1999-01-08 04:05:06', 1, .4),"

        # Afegim 100 mostres per a cada planta amb dades aleatories
        for j in range (3):
            for i in range(100):
                hum = random.randint(((10*(j+1))+10), (100 - 10*(j+1))) / 100
                queryHumidity += "(\'1999-01-08 04:" + str(int(i/60)) + ":" + str(int(i%60)) + "\', " + str(j+1) + ", " + str(hum) + "), "
        queryHumidity = queryHumidity[:-2] + ";"

        #Executem la query
        cursor.execute(queryHumidity, vars=None)

        # Query per a carregar informació de un log de reg
        queryWatering = "INSERT INTO Watering(time, plant_ID, water_applied) VALUES "
        queryWatering += "('1999-01-08 04:05:06', 1, 3),"

        # Afegim 100 mostres per a cada planta amb dades aleatories
        for j in range (3):
            for i in range(100):
                wat = 40 + op.mod(i, 20)
                queryWatering += "(\'1999-01-08 04:" + str(int(i/60)) + ":" + str(int(i%60)) + "\', " + str(j+1) + ", " + str(wat) + "), "
        queryWatering = queryWatering[:-2] + ";"

        #Executem la query
        cursor.execute(queryWatering, vars=None)

        # Guardem els canvis a la DB
        self.conn.commit()

        # Tanquem el cursor
        cursor.close()

    #Afegeix un conjunt de informació falsa per finalitats de testing del sistema
    def addTestData2(self):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()

        # Creem i executem la query per carregar les plantes de prova
        queryPlants = "INSERT INTO Plant(name, pot_number, since, watering_time, moisture_threshold, moisture_period, photo_period) VALUES "
        queryPlants += "('Rafflesia arnoldii', 1, '1999-01-08 04:05:06', 500, .7, 300, 200), "
        queryPlants += "('Dracaena cinnabari', 2, '1999-01-08 04:05:06', 10, .2, 600, 20);"
        cursor.execute(queryPlants)

        # Preparem i executem la query per carregar les imatges
        # Obrim les imatges
        image1 = open('images/1.jpg', 'rb').read()
        image2 = open('images/2.jpeg', 'rb').read()

        # Preparem i executem la query
        queryImages = "INSERT INTO Imatge(time, plant_ID, image, height, colour) VALUES "
        queryImages += "('1999-01-08 04:05:06', 1, %s, 35, ARRAY[255, 0, 0]),"
        queryImages += "('1999-01-09 04:05:06', 1, %s, 35, ARRAY[255, 0, 0]),"
        queryImages += "('1999-01-10 04:05:06', 1, %s, 35, ARRAY[255, 0, 0]),"
        queryImages += "('1999-01-08 04:05:06', 2, %s, 400, ARRAY[10, 255, 0]);"
        #cursor.execute(queryImages, (pg.Binary(image1), pg.Binary(image2), pg.Binary(image3), ))
        cursor.execute(queryImages,(str(base64.b64encode(image1))[2:-1],
                                    str(base64.b64encode(image2))[2:-1],
                                    str(base64.b64encode(image1))[2:-1],
                                    str(base64.b64encode(image2))[2:-1], ))

        # Query per a carregar informació de un log d'humitat
        queryHumidity = "INSERT INTO Humidity(time, plant_ID, value) VALUES "
        queryHumidity += "('1999-01-08 04:05:06', 1, .4),"

        # Afegim 100 mostres per a cada planta amb dades aleatories
        for j in range (2):
            for i in range(100):
                hum = random.randint(((10*(j+1))+10), (100 - 10*(j+1))) / 100
                queryHumidity += "(\'1999-01-08 04:" + str(int(i/60)) + ":" + str(int(i%60)) + "\', " + str(j+1) + ", " + str(hum) + "), "
        queryHumidity = queryHumidity[:-2] + ";"

        #Executem la query
        cursor.execute(queryHumidity, vars=None)

        # Query per a carregar informació de un log de reg
        queryWatering = "INSERT INTO Watering(time, plant_ID, water_applied) VALUES "
        queryWatering += "('1999-01-08 04:05:06', 1, 3),"

        # Afegim 100 mostres per a cada planta amb dades aleatories
        for j in range (2):
            for i in range(100):
                wat = 40 + op.mod(i, 20)
                queryWatering += "(\'1999-01-08 04:" + str(int(i/60)) + ":" + str(int(i%60)) + "\', " + str(j+1) + ", " + str(wat) + "), "
        queryWatering = queryWatering[:-2] + ";"

        #Executem la query
        cursor.execute(queryWatering, vars=None)

        # Guardem els canvis a la DB
        self.conn.commit()

        # Tanquem el cursor
        cursor.close()

    # Funció per pintar per pantalla tot el contingut de la taula indicada
    def printTable(self, name):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM ' + name + ';', vars=None)

        for row in cursor:
            print(list(row))
        cursor.close()

    # Funció que retorna un diccionari amb tota la informació guardada d'una planta concreta
    def getPlant(self, id):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()

        # Executem la query per obtenir la informació desitjada
        cursor.execute('SELECT * FROM plant WHERE plant_ID = %s;', (str(id),))

        # Creem el diccionari que emmagatema i retorna tota la informació
        resultat = {}
        for row in cursor:
            resultat = {
                "plant_ID": row[0],
                "name": row[1],
                "pot_number": row[2],
                "since": row[3],
                "watering_time": row[4],
                "moisture_threshold": row[5],
                "moisture_period": row[6],
                "photo_period": row[7]
                }

        cursor.close()
        return resultat

    def getActualPlants(self):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT plant_ID FROM plant WHERE (pot_number >= 1 and pot_number <= 3);""")

        resultat = []
        for row in cursor:
            resultat.append(int(row[0]))

        return resultat

    # Funció que afegeix una planta a la base de dades i retorna el ID que se li assigna per defecte
    def addPlant(self, name, pot_number, since, watering_time, moisture_threshold, moisture_period, photo_period):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()

        # Executem la query per obtenir la informació desitjada
        cursor.execute("""INSERT INTO Plant (name, pot_number, since, watering_time, moisture_threshold, moisture_period, photo_period)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)""", (name, str(pot_number), str(since), str(watering_time), str(moisture_threshold), str(moisture_period), str(photo_period), ))
        cursor.execute("""SELECT plant_id from plant where pot_number = %s""", (str(pot_number), ))

        # Creem el diccionari que emmagatema i retorna tota la informació
        resultat = -1
        for row in cursor:
            resultat = int(row[0])

        cursor.close()
        return resultat

    # Funció que retorna un array de diccionaris on cada un conté el timestamp i
    # valor d'una mostra d'humitat
    def getHumidityLog(self, id):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()
        cursor.execute("""SELECT h.time, h.value
                            FROM humidity h
                            INNER JOIN plant p ON p.plant_ID = h.plant_ID
                            WHERE h.plant_ID = %s
                            ORDER BY time ASC;""", (str(id), ))

        resultat = []
        for row in cursor:
            mostra = {
                "time": row[0],
                "value": row[1]
                }
            resultat.append(mostra)

        cursor.close()
        return resultat

    # Funció que retorna un diccionari amb el moment i el valor de la última
    # mesura d'humitat realitzada
    def getHumidityLast(self, id):
        # Obtenim l'objecte que permet executar les queries
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
                "value": row[2]
                }

        cursor.close()
        return resultat

    # Funció que retorna un diccionari amb el moment i el valor de la última
    # mesura d'humitat realitzada
    def getWateringLast(self, id):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()
        cursor.execute("""SELECT w.time, w.plant_ID, w.water_applied
                            FROM Watering w
                            INNER JOIN plant p ON p.plant_ID = w.plant_ID
                            WHERE w.plant_ID = %s
                            ORDER BY time DESC
                            LIMIT 1;""", (str(id), ))

        resultat = {}
        for row in cursor:
            resultat = {
                "time": row[0],
                "value": row[2]
                }

        cursor.close()
        return resultat

    def getLastPK(self):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()
        cursor.execute("""SELECT plant_id
                            FROM Plant
                            ORDER BY since DESC
                            LIMIT 1;""", vars=None)

        resultat = {}
        for row in cursor:
            resultat = int(row[0])

        cursor.close()
        return resultat

    def getImageLastTime(self, id):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()
        cursor.execute("""SELECT time
                            FROM Imatge
                            WHERE plant_ID = %s
                            ORDER BY time DESC
                            LIMIT 1;""", (str(id), ))

        resultat = -1
        for row in cursor:
            resultat = row[0]

        cursor.close()
        return resultat

    def getLastPlantAdded(self):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()
        cursor.execute("""SELECT plant_ID
                            FROM plant
                            ORDER BY since DESC
                            LIMIT 1;""", vars=None)

        resultat = -1
        for row in cursor:
            resultat = row[0]

        cursor.close()
        return resultat

    # Funció per afegir una nova mostra d'humitat
    def addHumidityMeasure(self, time, plant_id, value):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO Humidity (time, plant_ID, value)
                            VALUES (%s, %s, %s)""",
                            (str(time), str(plant_id), str(value),))
        self.conn.commit()
        cursor.close()

    # Funció per afegir una nova mostra d'humitat
    def addWateringValue(self, time, plant_id, value):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO Watering (time, plant_ID, water_applied)
                            VALUES (%s, %s, %s)""",
                            (str(time), str(plant_id), str(value),))
        self.conn.commit()
        cursor.close()

    # Funció per obtenir totes les imatges emmagatzemades d'una planta en un array
    # ALERT!!!: La funció pot petar fuerte, no testeada pero no necessaria
    def getImages(self, plant_id):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()


        cursor.execute("""SELECT image
                            FROM imatge
                            WHERE plant_ID = %s
                            ORDER BY time;""", (str(plant_id), ))

        resultat = []
        i = 0

        for row in cursor:
            #resultat.append(base64.b64decode(row[0]))
            #open(str(plant_id) + "_" + str(i) + ".jpg", 'wb').write(row[0])
            i += 1

        cursor.close()
        return resultat

    # Funció per a afegir una nova imatge a la DB
    def addImage(self, time, plant_id, image, height, colour):
        # Obtenim l'objecte que permet executar les queries
        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO Imatge (time, plant_ID, image, height, colour) VALUES
                            (%s, %s, %s, %s, %s)""",
                            (str(time), str(plant_id),
                            str( base64.b64encode(image))[2:-1], str(height), colour, ))
        self.conn.commit()
        cursor.close()


db = WeePlantDB()
#db.printTable("imatge")

#print(db.getHumidityLog(2))

db.resetTables()
db.addTestData2()
#print(db.getImages(1))
#print(db.getPlant(1))
#db.printTable('humidity')
db.closeDB()

#
