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
    # TODO: Implémenter la requête Neo4j
    print(f"Recherche de la fiche pour : {metier}")

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