import sqlite3, json
from plant_encoder import encode_image, decode_image


def insert_plant(id, raw_image, binary_image, masked_image, pruned_image,
                 branches_image, tips_image, height_image, skeleton_image,
                 metadata):
    try:
        connection = sqlite3.connect('./database/plant.db')
        cursor = connection.cursor()
        query = f"INSERT INTO plants (id, raw_image, binary_image, masked_image, pruned_image, branches_image, tips_image, height_image, skeleton_image, metadata) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(
            query, (id, encode_image(raw_image), encode_image(binary_image),
                    encode_image(masked_image), encode_image(pruned_image),
                    encode_image(branches_image), encode_image(tips_image),
                    encode_image(height_image), encode_image(skeleton_image),
                    json.dumps(metadata)))
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error insering data:", error)
    finally:
        if connection:
            connection.close()


def select_plants():
    try:
        connection = sqlite3.connect('./database/plant.db')
        cursor = connection.cursor()
        query = "SELECT * FROM plants"
        raw_imgs = []
        binary_imgs = []
        masked_imgs = []
        pruned_imgs = []
        branches_imgs = []
        tips_imgs = []
        height_imgs = []
        skeleton_imgs = []
        images = []
        for id, raw_image, binary_image, \
          masked_image, pruned_image, branches_image, \
           tips_image, height_image, skeleton_image, \
            metadata in cursor.execute(query):
            raw_imgs.append(decode_image((raw_image)))
            binary_imgs.append(decode_image((binary_image)))
            masked_imgs.append(decode_image((masked_image)))
            pruned_imgs.append(decode_image((pruned_image)))
            branches_imgs.append(decode_image((branches_image)))
            tips_imgs.append(decode_image((tips_image)))
            height_imgs.append(decode_image((height_image)))
            skeleton_imgs.append(decode_image((skeleton_image)))

        cursor.close()
        return [
            tuple(raw_imgs),
            tuple(binary_imgs),
            tuple(masked_imgs),
            tuple(pruned_imgs),
            tuple(branches_imgs),
            tuple(tips_imgs),
            tuple(height_imgs),
            tuple(skeleton_imgs),
        ]
    except sqlite3.Error as error:
        print("Error selecting data:", error)
    finally:
        if connection:
            connection.close()


def select_plants_data():
    try:
        connection = sqlite3.connect('./database/plant.db')
        cursor = connection.cursor()
        metadatas = []
        for row in cursor.execute("SELECT * FROM plants"):
            metadatas.append(row[-1])

        cursor.close()
        return metadatas
    except sqlite3.Error as error:
        print("Error selecting data:", error)
    finally:
        if connection:
            connection.close()