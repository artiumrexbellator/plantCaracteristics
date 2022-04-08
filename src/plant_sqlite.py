import sqlite3, json
from plant_encoder import encode_image, decode_image

# CREATE TABLE plants (
#     id             INTEGER PRIMARY KEY AUTOINCREMENT,
#     data           TEXT,
#     raw_image      BLOB,
#     binary_image   BLOB,
#     banches_image  BLOB,
#     masked_image   BLOB,
#     pruned_image   BLOB,
#     skeleton_image BLOB,
#     tips_image     BLOB,
#     height_image   BLOB
# );

def insert_plant(id, raw_image, binary_image, masked_image, pruned_image, branches_image, tips_image, height_image, skeleton_image, metadata):
	try:
		connection = sqlite3.connect('database/plant.db')
		cursor = connection.cursor()
		query = f"INSERT INTO plants (id, raw_image, binary_image, masked_image, pruned_image, branches_image, tips_image, height_image, skeleton_image, metadata) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
		cursor.execute(query, (
    	id, 
			encode_image(raw_image), 
			encode_image(binary_image), 
			encode_image(masked_image), 
			encode_image(pruned_image), 
			encode_image(branches_image), 
			encode_image(tips_image), 
			encode_image(height_image), 
			encode_image(skeleton_image), 
			json.dumps(metadata)
  	))
		connection.commit()
		cursor.close()
	except sqlite3.Error as error:
		print("Error insering data:", error)
	finally:
		if connection:
			connection.close()

def select_plants():
	try:
		connection = sqlite3.connect(f'database/plant.db')
		cursor = connection.cursor()
		query = "SELECT * FROM plants"
		images = []
		for id, raw_image, binary_image, masked_image, pruned_image, branches_image, tips_image, height_image, skeleton_image, metadata in cursor.execute(query):
			images.append({
				"id": id,
  			"raw_image": decode_image((raw_image)),
				"binary_image": decode_image((binary_image)),
				"masked_image": decode_image((masked_image)),
				"pruned_image": decode_image((pruned_image)),
				"branches_image": decode_image((branches_image)),
				"tips_image": decode_image((tips_image)),
				"height_image": decode_image((height_image)),
				"skeleton_image": decode_image((skeleton_image)),
				"metadata": json.loads(metadata)
			})
		cursor.close()
		return images
	except sqlite3.Error as error:
		print("Error selecting data:", error)
	finally:
		if connection:
			connection.close()

# def insertData(data: Tuple, name="plant"):
# 		try:
# 				connection = sqlite3.connect(f'{name}.db')
# 				cursor = connection.cursor()

# 				query = f"""INSERT INTO 
# 									plants (raw_image, binary_image, masked_image, pruned_image, branches_image, tips_image, height_image, skeleton_image, data) 
# 									VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

# 				cursor.execute(query, data)
# 				connection.commit()

# 				cursor.close()

# 		except sqlite3.Error as error:
# 				print("Failed to insert text data into sqlite table", error)
# 		finally:
# 				if connection:
# 						connection.close()
# 						print("the sqlite connection is closed")

# def getData(name="plant"):
# 		connection = sqlite3.connect(f'{name}.db')
# 		cursor = connection.cursor()
# 		query = "select * from plants"
# 		images = []
# 		for raw_image, binary_image, masked_image, pruned_image, branches_image, tips_image, height_image, skeleton_image, data in cursor.execute(
# 						query):
# 				images.append([
# 						decodeImage((raw_image)),
# 						decodeImage((binary_image)),
# 						decodeImage((masked_image)),
# 						decodeImage((pruned_image)),
# 						decodeImage((branches_image)),
# 						decodeImage((tips_image)),
# 						decodeImage((height_image)),
# 						decodeImage((skeleton_image)),
# 						json.loads(data)
# 				])
# 		cursor.close()
# 		return images

# # u can use frombuffer or fromstring,but frombuffer is optimal as long as fromstring will be deprecated for behavior reasons
# def decodeImage(imgBuff):
# 		nparr = np.frombuffer(imgBuff, np.uint8)
# 		img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
# 		return img_decode


# def createDb(name="plant"):
# 		try:
# 				conn = sqlite3.connect(f'{name}.db')
# 				c = conn.cursor()
# 				c.execute(
# 						'''CREATE TABLE plants (raw_image text, binary_image text, masked_image text, pruned_image text, branches_image text, tips_image text, height_image text, skeleton_image text,
# 				data text)''')
# 		except:
# 				pass


# if __name__ == "__main__":
		#createDb()
		#p = PlantChars()
		#p.loadImage("plants/plant.jpg")
		#insertData(p.fullImageTraitment())
		#p.fullImageTraitment()
		# cv2.imshow("winname", getData()[0][4])
		# k = cv2.waitKey(0)
