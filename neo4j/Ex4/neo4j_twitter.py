from py2neo import Graph
import csv

graph = Graph('bolt://localhost:7687')

graph.delete_all()

graph.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.idUser IS UNIQUE")
graph.run("CREATE CONSTRAINT IF NOT EXISTS FOR (t:Tweet) REQUIRE t.idTweet IS UNIQUE")
graph.run("CREATE CONSTRAINT IF NOT EXISTS FOR (h:Hashtag) REQUIRE h.name IS UNIQUE")

with open('/export/etu/alexandre.mione/BUT3/BDD/neo4j/tw_user.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file, delimiter='\t')
    for row in csv_reader:
        query = """
        CREATE (u:User {
            idUser: $idUser,
            screenName: $screenName,
            name: $name,
            description: $description,
            createdAt: $createdAt,
            url: $url,
            location: $location,
            lang: $lang,
            nbStatuses: toInteger($nbStatuses),
            nbFavorites: toInteger($nbFavorites),
            nbFollowers: toInteger($nbFollowers),
            nbFollowing: toInteger($nbFollowing)
        })
        """
        graph.run(query, parameters=row)

with open('/export/etu/alexandre.mione/BUT3/BDD/neo4j/tweet.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file, delimiter='<')
    
    for row in csv_reader:
        query_tweet = """
        MATCH (u:User {idUser: $idUser})
        CREATE (t:Tweet {
            idTweet: $idTweet,
            text: $text,
            createdAt: $createdAt,
            url: $url,
            source: $source,
            lang: $lang,
            nbRetweet: toInteger($nbRetweet),
            nbFavorites: toInteger($nbFavorites)
        })
        CREATE (u)-[:POSTED]->(t)
        """
        
        graph.run(query_tweet, parameters={
            'idUser': row['idUser'],
            'idTweet': row['idTweet'],
            'text': row['text'],
            'createdAt': row['createdAt'],
            'url': row['url'],
            'source': row['source'],
            'lang': row['lang'],
            'nbRetweet': row['nbRetweet'],
            'nbFavorites': row['nbFavorites']
        })
        
        if row['replyIdTweet'] and row['replyIdUser']:
            query_reply = """
            MATCH (t1:Tweet {idTweet: $idTweet})
            MATCH (t2:Tweet {idTweet: $replyIdTweet})
            CREATE (t1)-[:REPLY_TO]->(t2)
            """
            graph.run(query_reply, parameters={
                'idTweet': row['idTweet'],
                'replyIdTweet': row['replyIdTweet']
            })
        
        if row['quotedIdTweet'] and row['quotedIdUser']:
            query_quote = """
            MATCH (t1:Tweet {idTweet: $idTweet})
            MATCH (t2:Tweet {idTweet: $quotedIdTweet})
            CREATE (t1)-[:QUOTE]->(t2)
            """
            graph.run(query_quote, parameters={
                'idTweet': row['idTweet'],
                'quotedIdTweet': row['quotedIdTweet']
            })

with open('/export/etu/alexandre.mione/BUT3/BDD/neo4j/tweet_retweet.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file, delimiter='\t')
    
    for row in csv_reader:
        query = """
        MATCH (u:User {idUser: $idUser})
        MATCH (t:Tweet {idTweet: $idTweet})
        CREATE (u)-[:RETWEETED {
            idRetweet: $idRetweet,
            createdAt: $createdAt,
            urlEnd: $urlEnd,
            source: $source
        }]->(t)
        """
        graph.run(query, parameters=row)

with open('/export/etu/alexandre.mione/BUT3/BDD/neo4j/tweet_mention.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file, delimiter='\t')
    
    for row in csv_reader:
        query = """
        MATCH (t:Tweet {idTweet: $idTweet})
        MATCH (u:User {idUser: $idUser})
        CREATE (t)-[:MENTIONS {
            indiceStart: toInteger($indiceStart),
            indiceEnd: toInteger($indiceEnd)    
        }]->(u)
        """
        graph.run(query, parameters=row)

with open('/export/etu/alexandre.mione/BUT3/BDD/neo4j/tweet_hashtag.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file, delimiter='\t')
    
    for row in csv_reader:
        query_hashtag = """
        MERGE (h:Hashtag {name: $hashtag})
        """
        graph.run(query_hashtag, parameters={'hashtag': row['hashtag']})
        
        query_relation = """
        MATCH (t:Tweet {idTweet: $idTweet})
        MATCH (h:Hashtag {name: $hashtag})
        CREATE (t)-[:HAS_HASHTAG {
            hashtagBrut: $hashtagBrut,
            indiceStart: toInteger($indiceStart),
            indiceEnd: toInteger($indiceEnd)
        }]->(h)
        """
        graph.run(query_relation, parameters=row)

with open('/export/etu/alexandre.mione/BUT3/BDD/neo4j/tw_user_follow.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file, delimiter='\t')
    
    for row in csv_reader:
        query = """
        MATCH (u1:User {idUser: $sourceIdUser})
        MATCH (u2:User {idUser: $targetIdUser})
        CREATE (u1)-[:FOLLOWS]->(u2)
        """
        graph.run(query, parameters=row)

print("Import terminé !")

# EXERCICES #

# 1. Donner le nombre des utilisateurs
print("\n1. Nombre d'utilisateurs:")
query1 = "MATCH (u:User) RETURN count(u) as nbUsers"
result1 = graph.run(query1).data()
print(f"   {result1[0]['nbUsers']} utilisateurs")

# 2. Donner le nombre de tweets
print("\n2. Nombre de tweets:")
query2 = "MATCH (t:Tweet) RETURN count(t) as nbTweets"
result2 = graph.run(query2).data()
print(f"   {result2[0]['nbTweets']} tweets")

# 3. Donner le nombre d'hashtags
print("\n3. Nombre d'hashtags:")
query3 = "MATCH (h:Hashtag) RETURN count(h) as nbHashtags"
result3 = graph.run(query3).data()
print(f"   {result3[0]['nbHashtags']} hashtags")

# 4. Donner le nombre de tweets contenant le hashtag "actualité"
print("\n4. Nombre de tweets contenant le hashtag 'actualite':")
query4 = """
MATCH (t:Tweet)-[:HAS_HASHTAG]->(h:Hashtag {name: 'actualite'})
RETURN count(t) as nbTweets
"""
result4 = graph.run(query4).data()
print(f"   {result4[0]['nbTweets']} tweets")

# 5. Donner le nombre d'utilisateurs différents qui ont tweeté un tweet contenant le hashtag "valls"
print("\n5. Nombre d'utilisateurs ayant tweeté avec le hashtag 'valls':")
query5 = """
MATCH (u:User)-[:POSTED]->(t:Tweet)-[:HAS_HASHTAG]->(h:Hashtag {name: 'valls'})
RETURN count(DISTINCT u) as nbUsers
"""
result5 = graph.run(query5).data()
print(f"   {result5[0]['nbUsers']} utilisateurs")

# 6. Donner les tweets qui sont des réponses à un autre tweet
print("\n6. Tweets qui sont des réponses:")
query6 = """
MATCH (t1:Tweet)-[:REPLY_TO]->(t2:Tweet)
RETURN t1.idTweet as idTweet, t1.text as text, t2.idTweet as replyTo
"""
result6 = graph.run(query6).data()
for tweet in result6:
    print(f"   Tweet {tweet['idTweet']} répond à {tweet['replyTo']}")
    print(f"   Texte: {tweet['text'][:80]}...")

# 7. Donner le nombre de followers de "Spinomade"
print("\n7. Nombre de followers de 'Spinomade':")
query7 = """
MATCH (u:User {screenName: 'Spinomade'})<-[:FOLLOWS]-(follower:User)
RETURN count(follower) as nbFollowers
"""
result7 = graph.run(query7).data()
print(f"   {result7[0]['nbFollowers']} followers")

# 8. Donner le nombre d'utilisateurs suivis par "Spinomade"
print("\n8. Nombre d'utilisateurs suivis par 'Spinomade':")
query8 = """
MATCH (u:User {screenName: 'Spinomade'})-[:FOLLOWS]->(following:User)
RETURN count(following) as nbFollowing
"""
result8 = graph.run(query8).data()
print(f"   {result8[0]['nbFollowing']} utilisateurs suivis")

# 9. Donner les noms des followers de "Spinomade"
print("\n9. Noms des followers de 'Spinomade':")
query9 = """
MATCH (u:User {screenName: 'Spinomade'})<-[:FOLLOWS]-(follower:User)
RETURN follower.screenName as screenName, follower.name as name
ORDER BY follower.screenName
"""
result9 = graph.run(query9).data()
for follower in result9:
    print(f"   - {follower['screenName']} ({follower['name']})")
