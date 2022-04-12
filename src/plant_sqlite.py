import sqlite3, json
from plant_encoder import encode_image, decode_image


def insert_plant(id, raw_image, binary_image, masked_image, pruned_image,
                 branches_image, tips_image, height_image, skeleton_image,
                 metadata):
    try:
        connection = sqlite3.connect('./plant.db')
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
        connection = sqlite3.connect('./plant.db')
        cursor = connection.cursor()
        query = "SELECT * FROM plants"
        images = []
        for id, raw_image, binary_image, masked_image, pruned_image, branches_image, tips_image, height_image, skeleton_image, metadata in cursor.execute(
                query):
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