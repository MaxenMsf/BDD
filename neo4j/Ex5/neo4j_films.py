from py2neo import Graph
import csv

graph = Graph('bolt://localhost:7687')

graph.delete_all()

graph.run("CREATE CONSTRAINT IF NOT EXISTS FOR (m:Movie) REQUIRE m.movieId IS UNIQUE")
graph.run("CREATE CONSTRAINT IF NOT EXISTS FOR (a:Actor) REQUIRE a.tmdbId IS UNIQUE")
graph.run("CREATE CONSTRAINT IF NOT EXISTS FOR (d:Director) REQUIRE d.tmdbId IS UNIQUE")
graph.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Person) REQUIRE p.tmdbId IS UNIQUE")
graph.run("CREATE CONSTRAINT IF NOT EXISTS FOR (g:Genre) REQUIRE g.name IS UNIQUE")
graph.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.userId IS UNIQUE")

with open('/export/etu/alexandre.mione/BUT3/BDD/neo4j/Ex5/movie.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        query = """
        CREATE (m:Movie {
            movieId: $movieId,
            title: $title,
            imdbId: $imdbId,
            imdbRating: toFloat($imdbRating),
            url: $url,
            revenue: toInteger($revenue),
            tmdbId: $tmdbId,
            plot: $plot,
            poster: $poster,
            released: $released,
            budget: toInteger($budget)
        })
        """
        graph.run(query, parameters=row)

with open('/export/etu/alexandre.mione/BUT3/BDD/neo4j/Ex5/Genre.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        query = """
        MERGE (g:Genre {name: $name})
        """
        graph.run(query, parameters=row)

with open('/export/etu/alexandre.mione/BUT3/BDD/neo4j/Ex5/in_genre.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        query = """
        MATCH (m:Movie {movieId: $movieId})
        MATCH (g:Genre {name: $genre})
        CREATE (m)-[:IN_GENRE]->(g)
        """
        graph.run(query, parameters=row)

with open('/export/etu/alexandre.mione/BUT3/BDD/neo4j/Ex5/Actor.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        query = """
        CREATE (a:Actor {
            tmdbId: $tmdbId,
            imdbId: $imdbId,
            name: $name,
            born: $born,
            died: $died,
            bornIn: $bornIn,
            url: $url
        })
        """
        graph.run(query, parameters=row)

with open('/export/etu/alexandre.mione/BUT3/BDD/neo4j/Ex5/acted_in.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        query = """
        MATCH (a:Actor {tmdbId: $tmdbId})
        MATCH (m:Movie {movieId: $movieId})
        CREATE (a)-[:ACTED_IN {role: $actor_role}]->(m)
        """
        graph.run(query, parameters=row)

with open('/export/etu/alexandre.mione/BUT3/BDD/neo4j/Ex5/Director.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        query = """
        CREATE (d:Director {
            tmdbId: $tmdbId,
            name: $name,
            born: $born,
            died: $died,
            bornIn: $bornIn,
            bio: $bio,
            poster: $poster,
            url: $url
        })
        """

with open('/export/etu/alexandre.mione/BUT3/BDD/neo4j/Ex5/directed.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        query = """
        MATCH (d:Director {tmdbId: $tmdbId})
        MATCH (m:Movie {movieId: $movieId})
        CREATE (d)-[:DIRECTED]->(m)
        """
        graph.run(query, parameters=row)

with open('/export/etu/alexandre.mione/BUT3/BDD/neo4j/Ex5/User.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        query = """
        CREATE (u:User {
            userId: $userId,
            name: $name
        })
        """
        graph.run(query, parameters=row)

with open('/export/etu/alexandre.mione/BUT3/BDD/neo4j/Ex5/rated.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        query = """
        MATCH (u:User {userId: $userId})
        MATCH (m:Movie {movieId: $movieId})
        CREATE (u)-[:RATED {
            rating: toFloat($rating),
            timestamp: toInteger($timestamp)
        }]->(m)
        """
        graph.run(query, parameters=row)

print("Import terminé !")