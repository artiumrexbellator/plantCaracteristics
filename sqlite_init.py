import sqlite3
from typing import Tuple

# def convertToBinaryData(filename):
#     # Convert digital data to binary format
#     with open(filename, 'rb') as file:
#         blobData = file.read()
#     return blobData

def insertBlob(data: Tuple):
    try:
      sqliteConnection = sqlite3.connect('plants.db')
      cursor = sqliteConnection.cursor()
      print("Connected to SQLite")

      query = f"""INSERT INTO 
									plants (raw_image, binary_image, masked_image, pruned_image, banches_image, tips_image, height_image, skeleton_image, data) 
									VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

      cursor.execute(query, data)
      sqliteConnection.commit()

      cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")

if __name__ == "__main__":
	insertBlob("")