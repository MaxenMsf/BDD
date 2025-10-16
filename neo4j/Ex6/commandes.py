from py2neo import Graph

# Connexion à Neo4j
graph = Graph('bolt://localhost')

def afficher_menu():
    """Affiche le menu principal"""
    print("\n" + "="*50)
    print("           SYSTÈME DE GESTION DES MÉTIERS")
    print("="*50)
    print("1. Fiche métier")
    print("2. Compétence/Connaissance")
    print("3. Similarité entre compétences")
    print("4. Similarité entre métiers")
    print("5. Recommandation métier")
    print("6. Mobilité professionnelle")
    print("0. Quitter")
    print("="*50)

def fiche_metier():
    """Affiche la fiche d'un métier"""
    print("\n--- FICHE MÉTIER ---")
    metier = input("Entrez le nom du métier : ")
    
    # Requête pour récupérer toutes les informations du métier
    query = """
    MATCH (o:Occupation)
    WHERE toLower(o.occupation) CONTAINS toLower($metier)
    OPTIONAL MATCH (o)-[:REQUIRES]->(s:Skill)
    OPTIONAL MATCH (o)-[:OPTIONAL_SKILL]->(os:Skill)
    OPTIONAL MATCH (o)-[:REQUIRES_KNOWLEDGE]->(k:Knowledge)
    OPTIONAL MATCH (o)-[:OPTIONAL_KNOWLEDGE]->(ok:Knowledge)
    RETURN o.occupation as nom, 
           o.code as code,
           o.alt as alternatives,
           collect(DISTINCT s.name) as competences_requises,
           collect(DISTINCT os.name) as competences_optionnelles,
           collect(DISTINCT k.name) as connaissances_requises,
           collect(DISTINCT ok.name) as connaissances_optionnelles
    """
    
    resultats = graph.run(query, metier=metier).data()
    
    if not resultats:
        print(f"\n❌ Aucun métier trouvé pour : {metier}")
        return
    
    # Affichage des résultats
    for i, metier_info in enumerate(resultats, 1):
        print(f"\n{'='*60}")
        print(f"📋 MÉTIER {i}: {metier_info['nom']}")
        print(f"{'='*60}")
        print(f"Code: {metier_info['code']}")
        
        if metier_info['alternatives']:
            print(f"\n🔄 Autres appellations:")
            appellations = [app.strip() for app in metier_info['alternatives'].split(',') if app.strip()]
            for appellation in appellations:
                print(f"   • {appellation}")
        
        if metier_info['competences_requises'] and metier_info['competences_requises'][0]:
            print(f"\n✅ Compétences requises:")
            for comp in metier_info['competences_requises']:
                if comp:
                    print(f"   • {comp}")
        
        if metier_info['competences_optionnelles'] and metier_info['competences_optionnelles'][0]:
            print(f"\n⭐ Compétences optionnelles:")
            for comp in metier_info['competences_optionnelles']:
                if comp:
                    print(f"   • {comp}")
        
        if metier_info['connaissances_requises'] and metier_info['connaissances_requises'][0]:
            print(f"\n📚 Connaissances requises:")
            for conn in metier_info['connaissances_requises']:
                if conn:
                    print(f"   • {conn}")
        
        if metier_info['connaissances_optionnelles'] and metier_info['connaissances_optionnelles'][0]:
            print(f"\n📖 Connaissances optionnelles:")
            for conn in metier_info['connaissances_optionnelles']:
                if conn:
                    print(f"   • {conn}")
    
    print(f"\n✨ {len(resultats)} métier(s) trouvé(s)")

def competence_connaissance():
    """Affiche les informations sur une compétence ou connaissance"""
    print("\n--- COMPÉTENCE/CONNAISSANCE ---")
    nom = input("Entrez le nom de la compétence ou connaissance : ")
    # TODO: Implémenter la requête Neo4j
    print(f"Recherche d'informations pour : {nom}")

def similarite_competences():
    """Calcule la similarité entre deux compétences"""
    print("\n--- SIMILARITÉ ENTRE COMPÉTENCES ---")
    comp1 = input("Première compétence : ")
    comp2 = input("Deuxième compétence : ")
    # TODO: Implémenter la requête Neo4j
    print(f"Calcul de similarité entre {comp1} et {comp2}")

def similarite_metiers():
    """Calcule la similarité entre deux métiers"""
    print("\n--- SIMILARITÉ ENTRE MÉTIERS ---")
    metier1 = input("Premier métier : ")
    metier2 = input("Deuxième métier : ")
    # TODO: Implémenter la requête Neo4j
    print(f"Calcul de similarité entre {metier1} et {metier2}")

def recommandation_metier():
    """Recommande des métiers basés sur des compétences"""
    print("\n--- RECOMMANDATION MÉTIER ---")
    competences = input("Entrez vos compétences (séparées par des virgules) : ")
    # TODO: Implémenter la requête Neo4j
    print(f"Recherche de métiers correspondants à : {competences}")

def mobilite_professionnelle():
    """Analyse la mobilité professionnelle"""
    print("\n--- MOBILITÉ PROFESSIONNELLE ---")
    metier_actuel = input("Métier actuel : ")
    # TODO: Implémenter la requête Neo4j
    print(f"Analyse de mobilité depuis : {metier_actuel}")

def main():
    """Fonction principale"""
    while True:
        afficher_menu()
        choix = input("\nVotre choix : ")
        
        if choix == "1":
            fiche_metier()
        elif choix == "2":
            competence_connaissance()
        elif choix == "3":
            similarite_competences()
        elif choix == "4":
            similarite_metiers()
        elif choix == "5":
            recommandation_metier()
        elif choix == "6":
            mobilite_professionnelle()
        elif choix == "0":
            print("\nAu revoir !")
            break
        else:
            print("\nChoix invalide. Veuillez réessayer.")
        
        input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()