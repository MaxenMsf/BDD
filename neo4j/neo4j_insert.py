from py2neo import Graph

graph = Graph('bolt://localhost:7687')

graph.delete_all()

node_queries = [
    "MERGE (:Personne {nom: 'Bob', age: 33})",
    "MERGE (:Personne {nom: 'Alice', age: 18})",
    "MERGE (:Personne {nom: 'Ben', age: 25})",
    "MERGE (:Vehicule {type: 'voiture', modele: 'clio'})",
    "MERGE (:Vehicule {type: 'moto', modele: 'R1'})",
    "MERGE (:Vehicule {type: 'voiture', modele: 'A4'})",
]

for q in node_queries:
    graph.run(q)

rel_queries = [
    "MATCH (p:Personne {nom: 'Bob'}),  (v:Vehicule {modele: 'clio'}) MERGE (p)-[:Posseder {depuis: 2014}]->(v)",
    "MATCH (p:Personne {nom: 'Alice'}),(v:Vehicule {modele: 'R1'})   MERGE (p)-[:Posseder {depuis: 2007}]->(v)",
    "MATCH (p:Personne {nom: 'Ben'}),  (v:Vehicule {modele: 'A4'})   MERGE (p)-[:Posseder {depuis: 2010}]->(v)",

    "MATCH (p:Personne {nom: 'Bob'}),  (v:Vehicule {modele: 'clio'}) MERGE (p)-[:Conduire]->(v)",
    "MATCH (p:Personne {nom: 'Alice'}),(v:Vehicule {modele: 'R1'})   MERGE (p)-[:Conduire]->(v)",
    "MATCH (p:Personne {nom: 'Ben'}),  (v:Vehicule {modele: 'A4'})   MERGE (p)-[:Conduire]->(v)",
    "MATCH (p:Personne {nom: 'Alice'}),(v:Vehicule {modele: 'clio'}) MERGE (p)-[:Conduire]->(v)",
]

for q in rel_queries:
    graph.run(q)