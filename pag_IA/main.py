
import psycopg2

# Establece la conexión con la base de datos PostgreSQL
conn = psycopg2.connect(
    user="postgres",
    password="Yamile25",
    host="localhost",
    port="5432",
    database="meme"
)

# Crea un cursor
cur = conn.cursor()

# Ruta de la imagen
imagen_path = "babosa_2.jpg"
description = "Descripción del meme"
title = "Título del meme"

# Insertar la ruta de la imagen y otros datos en la tabla meme
query = "INSERT INTO meme (description, image, title) VALUES (%s, %s, %s)"
valores = (description, imagen_path, title)

# Ejecutar la consulta SQL
cur.execute(query, valores)

# Confirmar los cambios en la base de datos
conn.commit()

# Cerrar el cursor y la conexión
cur.close()
conn.close()

print("La ruta de la imagen y los datos se han almacenado correctamente en la base de datos.")