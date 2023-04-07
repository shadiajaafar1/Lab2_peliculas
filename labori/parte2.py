import networkx as nx
import pandas as pd

# Carga el conjunto de datos de IMDB Top 250 Movies desde un archivo CSV
df = pd.read_csv('imdb_top250.csv')

# Crea un grafo dirigido para representar la relación entre directores y películas
graph = nx.DiGraph()

# Agrega nodos de directores y géneros al grafo
directors = set()
genres = set()
for index, row in df.iterrows():
    for director in row['directors'].split(', '):
        graph.add_node(director, bipartite=0)
        directors.add(director)
    for genre in row['genre'].split(', '):
        graph.add_node(genre, bipartite=1)
        genres.add(genre)

# Agrega arcos entre los nodos de directores y géneros
for index, row in df.iterrows():
    for director in row['directors'].split(', '):
        for genre in row['genre'].split(', '):
            graph.add_edge(director, genre)

# Función que calcula la probabilidad de que dos directores colaboren en una película de un género específico
def calculate_collaboration_probability(director1, director2, genre):
    # Obtener lista de directores que hayan trabajado en películas del género dado
    genre_directors = [n for n, d in graph.nodes(data=True) if d['bipartite'] == 0 and genre in graph[n]]
    # Verificar si los dos directores dados han trabajado juntos antes
    if director1 not in genre_directors or director2 not in genre_directors:
        return "Al menos uno de los directores no ha trabajado en películas de este género."
    elif graph.has_edge(director1, director2):
        return "Los directores han trabajado juntos antes, por lo que es probable que colaboren de nuevo en una película de este género."
    else:
        # Obtener la subgráfica inducida por los directores del género
        subgraph = graph.subgraph(genre_directors)
        # Calcular la medida de cercanía entre los dos directores en la subgráfica
        try:
            closeness = nx.closeness_centrality(subgraph, u=director1, distance='weight')[director2]
            # Escalar la medida de cercanía para que esté en el rango [0,1]
            probability = closeness / (len(subgraph.nodes) - 1)
            return f"La probabilidad de que los directores colaboren en una película de este género es del {probability:.2%}."
        except nx.NetworkXError:
            return "Error al calcular la medida de cercanía entre los directores."

# Preguntar al usuario qué director y género quiere introducir
director1 = input("Introduce el primer director: ")
director2 = input("Introduce el segundo director: ")
genre = input("Introduce el género: ")

# Ejemplo de uso: calcular la probabilidad de que Quentin Tarantino y Christopher Nolan colaboren en una película de acción
print(calculate_collaboration_probability(director1, director2, genre))






       











