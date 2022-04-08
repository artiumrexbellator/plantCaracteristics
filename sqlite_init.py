import sqlite3
from typing import Tuple
from PlantChars import PlantChars
import json
import numpy as np
import cv2

# def convertToBinaryData(filename):
#     # Convert digital data to binary format
#     with open(filename, 'rb') as file:
#         textData = file.read()
#     return textData


# u can use frombuffer or fromstring,but frombuffer is optimal as long as fromstring will be deprecated for behavior reasons
def decodeImage(imgBuff):
    nparr = np.frombuffer(imgBuff, np.uint8)
    img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_decode


def createDb(name="plant"):
    try:
        conn = sqlite3.connect(f'{name}.db')
        c = conn.cursor()
        c.execute(
            '''CREATE TABLE plants (raw_image text, binary_image text, masked_image text, pruned_image text, branches_image text, tips_image text, height_image text, skeleton_image text,
        data text)''')
    except:
        pass


def insertData(data: Tuple, name="plant"):
    try:
        sqliteConnection = sqlite3.connect(f'{name}.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        query = f"""INSERT INTO 
									plants (raw_image, binary_image, masked_image, pruned_image, branches_image, tips_image, height_image, skeleton_image, data) 
									VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        cursor.execute(query, data)
        sqliteConnection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert text data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def getData(name="plant"):
    sqliteConnection = sqlite3.connect(f'{name}.db')
    cursor = sqliteConnection.cursor()
    query = "select * from plants"
    images = []
    for raw_image, binary_image, masked_image, pruned_image, branches_image, tips_image, height_image, skeleton_image, data in cursor.execute(
            query):
        images.append([
            decodeImage((raw_image)),
            decodeImage((binary_image)),
            decodeImage((masked_image)),
            decodeImage((pruned_image)),
            decodeImage((branches_image)),
            decodeImage((tips_image)),
            decodeImage((height_image)),
            decodeImage((skeleton_image)),
            json.loads(data)
        ])
    cursor.close()
    return images


if __name__ == "__main__":
    #createDb()
    #p = PlantChars()
    #p.loadImage("plants/plant.jpg")
    #insertData(p.fullImageTraitment())
    #p.fullImageTraitment()
    cv2.imshow("winname", getData()[0][4])
    k = cv2.waitKey(0)
