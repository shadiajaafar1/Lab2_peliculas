import pandas as pd

# Leer archivo CSV
movies_df = pd.read_csv("imdb_top250.csv")

# Obtener lista de directores y géneros
directors = list(movies_df["directors"].unique())
genres = list(movies_df["genre"].unique())

# Crear diccionario de árbol de director y género
director_tree = {}
for director in directors:
    director_movies = movies_df[movies_df["directors"] == director]
    director_tree[director] = {}
    for index, row in director_movies.iterrows():
        genres = ", ".join(sorted(row["genre"].split(", ")))
        if genres not in director_tree[director]:
            director_tree[director][genres] = {}
        director_tree[director][genres][row["name"]] = row["rating"]

# Función para encontrar los géneros a N niveles de un director
def find_genres(director, levels):
    visited = set()
    queue = [(director, "ROOT")]
    while queue:
        cur, parent_genre = queue.pop(0)
        if cur not in director_tree:
            continue
        for genre_movies in director_tree[cur]:
            if any(genre in genre_movies.split(", ") for genre in visited):
                continue
            visited.add(genre_movies)
            if parent_genre != "ROOT":
                visited.add(parent_genre)
            if levels == levels:
                return set(genre_movies.split(","))
            for title in director_tree[cur][genre_movies]:
                queue.append((title, genre_movies))
    return set()

# Pedir al usuario el nombre del director y el número de niveles
director = input("Ingrese el nombre del director: ")
levels = int(input("Ingrese el número de niveles: "))

# Obtener los géneros a N niveles del director
genres = find_genres(director, levels)

# Imprimir los géneros encontrados
print(genres)









