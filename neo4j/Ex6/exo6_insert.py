from py2neo import Graph
import pandas as pd

graph = Graph('bolt://localhost')

graph.delete_all()

df = pd.read_csv('full_occupation_fr.csv')

for index, row in df.iterrows():
    occupation_query = """
    CREATE (o:Occupation)
    SET o.code = $code,
        o.occupation = $occupation,
        o.alt = $alt,
        o.id = $id
    """
    graph.run(occupation_query, 
              code=row['code'], 
              occupation=row['occupation'] if pd.notna(row['occupation']) else '',
              alt=row['alt'] if pd.notna(row['alt']) else '',
              id=index)
    
    if pd.notna(row['requeredSkills']) and row['requeredSkills'] != 'none':
        skills = [s.strip() for s in row['requeredSkills'].split(',')]
        for skill in skills:
            skill_query = """
            MATCH (o:Occupation {id: $id})
            MERGE (s:Skill {name: $skill})
            MERGE (o)-[:REQUIRES]->(s)
            """
            graph.run(skill_query, id=index, skill=skill)
    
    if pd.notna(row['optionalSkills']) and row['optionalSkills'] != 'none':
        skills = [s.strip() for s in row['optionalSkills'].split(',')]
        for skill in skills:
            skill_query = """
            MATCH (o:Occupation {id: $id})
            MERGE (s:Skill {name: $skill})
            MERGE (o)-[:OPTIONAL_SKILL]->(s)
            """
            graph.run(skill_query, id=index, skill=skill)
    
    if pd.notna(row['requeredKnowledges']) and row['requeredKnowledges'] != 'none':
        knowledges = [k.strip() for k in row['requeredKnowledges'].split(',')]
        for knowledge in knowledges:
            knowledge_query = """
            MATCH (o:Occupation {id: $id})
            MERGE (k:Knowledge {name: $knowledge})
            MERGE (o)-[:REQUIRES_KNOWLEDGE]->(k)
            """
            graph.run(knowledge_query, id=index, knowledge=knowledge)
    
    if pd.notna(row['optionalKnowledge']) and row['optionalKnowledge'] != 'none':
        knowledges = [k.strip() for k in row['optionalKnowledge'].split(',')]
        for knowledge in knowledges:
            knowledge_query = """
            MATCH (o:Occupation {id: $id})
            MERGE (k:Knowledge {name: $knowledge})
            MERGE (o)-[:OPTIONAL_KNOWLEDGE]->(k)
            """
            graph.run(knowledge_query, id=index, knowledge=knowledge)
    
    print(f"Traité: {row['occupation']} ({index + 1}/{len(df)})")

print("Import terminé!")