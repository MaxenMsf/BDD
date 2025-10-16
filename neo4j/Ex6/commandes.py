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
    query_skill = """
    MATCH (s:Skill)
    WHERE toLower(s.name) CONTAINS toLower($nom)
    OPTIONAL MATCH (o1:Occupation)-[:REQUIRES]->(s)
    OPTIONAL MATCH (o2:Occupation)-[:OPTIONAL_SKILL]->(s)
    RETURN s.name as nom,
           'Compétence' as type,
           collect(DISTINCT o1.occupation) as metiers_requis,
           collect(DISTINCT o2.occupation) as metiers_optionnels
    """
    query_knowledge = """
    MATCH (k:Knowledge)
    WHERE toLower(k.name) CONTAINS toLower($nom)
    OPTIONAL MATCH (o1:Occupation)-[:REQUIRES_KNOWLEDGE]->(k)
    OPTIONAL MATCH (o2:Occupation)-[:OPTIONAL_KNOWLEDGE]->(k)
    RETURN k.name as nom,
           'Connaissance' as type,
           collect(DISTINCT o1.occupation) as metiers_requis,
           collect(DISTINCT o2.occupation) as metiers_optionnels
    """
    resultats_skills = graph.run(query_skill, nom=nom).data()
    resultats_knowledge = graph.run(query_knowledge, nom=nom).data()
    
    tous_resultats = resultats_skills + resultats_knowledge
    
    if not tous_resultats:
        print(f"\n❌ Aucune compétence ou connaissance trouvée pour : {nom}")
        return
    
    for i, item in enumerate(tous_resultats, 1):
        print(f"\n{'='*60}")
        print(f"📋 {item['type'].upper()} {i}: {item['nom']}")
        print(f"{'='*60}")
        metiers_requis = [m for m in item['metiers_requis'] if m]
        if metiers_requis:
            print(f"\n✅ Requise pour {len(metiers_requis)} métier(s):")
            for metier in sorted(metiers_requis):
                print(f"   • {metier}")
        
        metiers_optionnels = [m for m in item['metiers_optionnels'] if m]
        if metiers_optionnels:
            print(f"\n⭐ Optionnelle pour {len(metiers_optionnels)} métier(s):")
            for metier in sorted(metiers_optionnels):
                print(f"   • {metier}")
        
        if not metiers_requis and not metiers_optionnels:
            print(f"\n❓ Cette {item['type'].lower()} n'est associée à aucun métier dans la base de données.")
    
    print(f"\n✨ {len(tous_resultats)} élément(s) trouvé(s)")

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
    
    query = """
    MATCH (o1:Occupation), (o2:Occupation)
    WHERE toLower(o1.occupation) CONTAINS toLower($metier1)
    AND toLower(o2.occupation) CONTAINS toLower($metier2)
    
    OPTIONAL MATCH (o1)-[:REQUIRES]->(s1:Skill)
    OPTIONAL MATCH (o1)-[:OPTIONAL_SKILL]->(os1:Skill)
    OPTIONAL MATCH (o1)-[:REQUIRES_KNOWLEDGE]->(k1:Knowledge)
    OPTIONAL MATCH (o1)-[:OPTIONAL_KNOWLEDGE]->(ok1:Knowledge)
    
    OPTIONAL MATCH (o2)-[:REQUIRES]->(s2:Skill)
    OPTIONAL MATCH (o2)-[:OPTIONAL_SKILL]->(os2:Skill)
    OPTIONAL MATCH (o2)-[:REQUIRES_KNOWLEDGE]->(k2:Knowledge)
    OPTIONAL MATCH (o2)-[:OPTIONAL_KNOWLEDGE]->(ok2:Knowledge)
    
    RETURN o1.occupation as metier1_nom,
           o2.occupation as metier2_nom,
           collect(DISTINCT s1.name) + collect(DISTINCT os1.name) + 
           collect(DISTINCT k1.name) + collect(DISTINCT ok1.name) as competences1,
           collect(DISTINCT s2.name) + collect(DISTINCT os2.name) + 
           collect(DISTINCT k2.name) + collect(DISTINCT ok2.name) as competences2
    """
    
    resultats = graph.run(query, metier1=metier1, metier2=metier2).data()
    
    if not resultats:
        print(f"\n❌ Impossible de trouver les deux métiers : {metier1} et {metier2}")
        return
    
    for resultat in resultats:
        metier1_nom = resultat['metier1_nom']
        metier2_nom = resultat['metier2_nom']
        
        competences1 = set([comp for comp in resultat['competences1'] if comp])
        competences2 = set([comp for comp in resultat['competences2'] if comp])
        
        print(f"\n{'='*70}")
        print(f"📊 COMPARAISON DE SIMILARITÉ")
        print(f"{'='*70}")
        print(f"🔵 Métier 1: {metier1_nom}")
        print(f"🔴 Métier 2: {metier2_nom}")
        print(f"{'='*70}")
        
        intersection = competences1.intersection(competences2)
        union = competences1.union(competences2)
        
        if len(union) == 0:
            similarite_jaccard = 0.0
        else:
            similarite_jaccard = len(intersection) / len(union)
        
        print(f"\n📈 RÉSULTATS DE LA SIMILARITÉ DE JACCARD:")
        print(f"   • Compétences/connaissances du métier 1: {len(competences1)}")
        print(f"   • Compétences/connaissances du métier 2: {len(competences2)}")
        print(f"   • Compétences/connaissances communes: {len(intersection)}")
        print(f"   • Total unique (union): {len(union)}")
        print(f"   • Similarité de Jaccard: {similarite_jaccard:.3f} ({similarite_jaccard*100:.1f}%)")
        
        if similarite_jaccard >= 0.7:
            interpretation = "🟢 Très similaires"
        elif similarite_jaccard >= 0.5:
            interpretation = "🟡 Assez similaires"
        elif similarite_jaccard >= 0.3:
            interpretation = "🟠 Peu similaires"
        else:
            interpretation = "🔴 Très différents"
        
        print(f"   • Interprétation: {interpretation}")
        
        if intersection:
            print(f"\n🤝 COMPÉTENCES/CONNAISSANCES COMMUNES ({len(intersection)}):")
            for comp in sorted(intersection):
                print(f"   • {comp}")
        
        specifiques1 = competences1 - competences2
        if specifiques1:
            print(f"\n🔵 SPÉCIFIQUES AU MÉTIER 1 ({len(specifiques1)}):")
            for comp in sorted(specifiques1):
                print(f"   • {comp}")
        
        specifiques2 = competences2 - competences1
        if specifiques2:
            print(f"\n🔴 SPÉCIFIQUES AU MÉTIER 2 ({len(specifiques2)}):")
            for comp in sorted(specifiques2):
                print(f"   • {comp}")
    
    print(f"\n✨ Analyse terminée")

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
    metier_cible = input("Métier cible : ")
    
    query_check_actuel = """
    MATCH (o:Occupation)
    WHERE toLower(o.occupation) CONTAINS toLower($metier)
    RETURN o.occupation as nom
    LIMIT 1
    """
    
    query_check_cible = """
    MATCH (o:Occupation)
    WHERE toLower(o.occupation) CONTAINS toLower($metier)
    RETURN o.occupation as nom
    LIMIT 1
    """
    
    metier_actuel_trouve = graph.run(query_check_actuel, metier=metier_actuel).data()
    metier_cible_trouve = graph.run(query_check_cible, metier=metier_cible).data()
    
    if not metier_actuel_trouve:
        print(f"\n❌ Métier actuel non trouvé : {metier_actuel}")
        print("💡 Suggestion : Vérifiez l'orthographe ou essayez avec des mots-clés plus généraux")
        return
    
    if not metier_cible_trouve:
        print(f"\n❌ Métier cible non trouvé : {metier_cible}")
        print("💡 Suggestion : Vérifiez l'orthographe ou essayez avec des mots-clés plus généraux")
        return
    
    query = """
    MATCH (o_actuel:Occupation), (o_cible:Occupation)
    WHERE toLower(o_actuel.occupation) CONTAINS toLower($metier_actuel)
    AND toLower(o_cible.occupation) CONTAINS toLower($metier_cible)
    
    OPTIONAL MATCH (o_actuel)-[:REQUIRES]->(s_actuel:Skill)
    OPTIONAL MATCH (o_actuel)-[:OPTIONAL_SKILL]->(os_actuel:Skill)
    OPTIONAL MATCH (o_actuel)-[:REQUIRES_KNOWLEDGE]->(k_actuel:Knowledge)
    OPTIONAL MATCH (o_actuel)-[:OPTIONAL_KNOWLEDGE]->(ok_actuel:Knowledge)
    
    OPTIONAL MATCH (o_cible)-[:REQUIRES]->(s_cible:Skill)
    OPTIONAL MATCH (o_cible)-[:OPTIONAL_SKILL]->(os_cible:Skill)
    OPTIONAL MATCH (o_cible)-[:REQUIRES_KNOWLEDGE]->(k_cible:Knowledge)
    OPTIONAL MATCH (o_cible)-[:OPTIONAL_KNOWLEDGE]->(ok_cible:Knowledge)
    
    RETURN o_actuel.occupation as metier_actuel_nom,
           o_cible.occupation as metier_cible_nom,
           collect(DISTINCT s_actuel.name) + collect(DISTINCT os_actuel.name) + 
           collect(DISTINCT k_actuel.name) + collect(DISTINCT ok_actuel.name) as competences_actuelles,
           collect(DISTINCT s_cible.name) + collect(DISTINCT os_cible.name) + 
           collect(DISTINCT k_cible.name) + collect(DISTINCT ok_cible.name) as competences_cibles,
           collect(DISTINCT s_cible.name) + collect(DISTINCT k_cible.name) as competences_cibles_requises,
           collect(DISTINCT os_cible.name) + collect(DISTINCT ok_cible.name) as competences_cibles_optionnelles
    """
    
    resultats = graph.run(query, metier_actuel=metier_actuel, metier_cible=metier_cible).data()
    
    if not resultats:
        print(f"\n❌ Erreur lors de l'analyse des métiers")
        return
    
    for resultat in resultats:
        metier_actuel_nom = resultat['metier_actuel_nom']
        metier_cible_nom = resultat['metier_cible_nom']
        
        competences_actuelles = set([comp for comp in resultat['competences_actuelles'] if comp])
        competences_cibles = set([comp for comp in resultat['competences_cibles'] if comp])
        competences_cibles_requises = set([comp for comp in resultat['competences_cibles_requises'] if comp])
        competences_cibles_optionnelles = set([comp for comp in resultat['competences_cibles_optionnelles'] if comp])
        
        print(f"\n{'='*70}")
        print(f"🎯 ANALYSE DE MOBILITÉ PROFESSIONNELLE")
        print(f"{'='*70}")
        print(f"📍 Métier actuel: {metier_actuel_nom}")
        print(f"🎯 Métier cible: {metier_cible_nom}")
        print(f"{'='*70}")
        
        competences_communes = competences_actuelles.intersection(competences_cibles)
        
        competences_manquantes = competences_cibles - competences_actuelles
        competences_manquantes_requises = competences_cibles_requises - competences_actuelles
        competences_manquantes_optionnelles = competences_cibles_optionnelles - competences_actuelles
        
        if len(competences_cibles) == 0:
            pourcentage_matching = 100.0
        else:
            pourcentage_matching = (len(competences_communes) / len(competences_cibles)) * 100
        
        if len(competences_cibles_requises) == 0:
            pourcentage_matching_requis = 100.0
        else:
            competences_communes_requises = competences_actuelles.intersection(competences_cibles_requises)
            pourcentage_matching_requis = (len(competences_communes_requises) / len(competences_cibles_requises)) * 100
        
        print(f"\n📊 RÉSULTATS DU MATCHING:")
        print(f"   • Compétences du métier actuel: {len(competences_actuelles)}")
        print(f"   • Compétences du métier cible: {len(competences_cibles)}")
        print(f"   • Compétences déjà acquises: {len(competences_communes)}")
        print(f"   • Compétences manquantes: {len(competences_manquantes)}")
        print(f"   • Matching global: {pourcentage_matching:.1f}%")
        print(f"   • Matching compétences requises: {pourcentage_matching_requis:.1f}%")
        
        if pourcentage_matching >= 80:
            faisabilite = "🟢 Transition très facile"
        elif pourcentage_matching >= 60:
            faisabilite = "🟡 Transition modérée"
        elif pourcentage_matching >= 40:
            faisabilite = "🟠 Transition difficile"
        else:
            faisabilite = "🔴 Transition très difficile"
        
        print(f"   • Faisabilité: {faisabilite}")
        
        if competences_communes:
            print(f"\n✅ COMPÉTENCES DÉJÀ ACQUISES ({len(competences_communes)}):")
            for comp in sorted(competences_communes):
                print(f"   • {comp}")
        
        if competences_manquantes_requises:
            print(f"\n🚨 COMPÉTENCES MANQUANTES REQUISES ({len(competences_manquantes_requises)}):")
            print("   ⚠️  PRIORITÉ HAUTE - Indispensables pour le poste")
            for comp in sorted(competences_manquantes_requises):
                print(f"   • {comp}")
        
        if competences_manquantes_optionnelles:
            print(f"\n📚 COMPÉTENCES MANQUANTES OPTIONNELLES ({len(competences_manquantes_optionnelles)}):")
            print("   💡 PRIORITÉ BASSE - Recommandées mais non indispensables")
            for comp in sorted(competences_manquantes_optionnelles):
                print(f"   • {comp}")
        
        print(f"\n💡 RECOMMANDATIONS:")
        if pourcentage_matching_requis == 100:
            print("   🎉 Toutes les compétences requises sont acquises !")
            if competences_manquantes_optionnelles:
                print("   📖 Concentrez-vous sur les compétences optionnelles pour vous démarquer")
            else:
                print("   ✨ Vous êtes parfaitement qualifié pour ce métier !")
        else:
            print("   🎯 Concentrez-vous d'abord sur les compétences requises manquantes")
            if len(competences_manquantes_requises) <= 3:
                print("   👍 Peu de compétences requises à acquérir - transition réalisable")
            else:
                print("   ⚠️  Beaucoup de compétences requises à acquérir - formation approfondie nécessaire")
        
        competences_transferables = competences_actuelles - competences_cibles
        if competences_transferables:
            print(f"\n🔄 COMPÉTENCES TRANSFÉRABLES ({len(competences_transferables)}):")
            print("   💼 Ces compétences pourraient être valorisées autrement")
            for comp in sorted(competences_transferables):
                print(f"   • {comp}")
    
    print(f"\n✨ Analyse de mobilité terminée")

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