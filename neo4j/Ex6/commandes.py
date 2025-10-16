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
    
    # Requête pour trouver les métiers qui utilisent chaque compétence
    query = """
    MATCH (s1:Skill)
    WHERE toLower(s1.name) CONTAINS toLower($comp1)
    MATCH (s2:Skill)
    WHERE toLower(s2.name) CONTAINS toLower($comp2)
    
    // Métiers associés à la compétence 1 (requise ou optionnelle)
    OPTIONAL MATCH (o1:Occupation)-[:REQUIRES]->(s1)
    OPTIONAL MATCH (o1_opt:Occupation)-[:OPTIONAL_SKILL]->(s1)
    WITH s1, s2, collect(DISTINCT o1) + collect(DISTINCT o1_opt) as metiers_comp1
    
    // Métiers associés à la compétence 2 (requise ou optionnelle)
    OPTIONAL MATCH (o2:Occupation)-[:REQUIRES]->(s2)
    OPTIONAL MATCH (o2_opt:Occupation)-[:OPTIONAL_SKILL]->(s2)
    WITH s1, s2, metiers_comp1, collect(DISTINCT o2) + collect(DISTINCT o2_opt) as metiers_comp2
    
    // Calcul de l'intersection (métiers communs)
    WITH s1, s2, metiers_comp1, metiers_comp2,
         [m IN metiers_comp1 WHERE m IN metiers_comp2] as intersection
    
    // Calcul de l'union (tous les métiers distincts)
    WITH s1, s2, metiers_comp1, metiers_comp2, intersection,
         [m IN metiers_comp1 + metiers_comp2] as union_list
    
    // Dédupliquer l'union
    WITH s1, s2, metiers_comp1, metiers_comp2, intersection,
         [m IN union_list | m] as all_metiers
    UNWIND all_metiers as metier
    WITH s1, s2, metiers_comp1, metiers_comp2, intersection, 
         collect(DISTINCT metier) as union
    
    RETURN s1.name as competence1,
           s2.name as competence2,
           size(metiers_comp1) as nb_metiers_comp1,
           size(metiers_comp2) as nb_metiers_comp2,
           size(intersection) as nb_intersection,
           size(union) as nb_union,
           CASE 
               WHEN size(union) = 0 THEN 0.0
               ELSE toFloat(size(intersection)) / toFloat(size(union))
           END as similarite_jaccard,
           [m IN intersection | m.occupation] as metiers_communs
    """
    
    resultats = graph.run(query, comp1=comp1, comp2=comp2).data()
    
    if not resultats or not resultats[0]['competence1'] or not resultats[0]['competence2']:
        print(f"\n❌ Une ou les deux compétences n'ont pas été trouvées")
        return
    
    # Affichage des résultats
    for result in resultats:
        print(f"\n{'='*70}")
        print(f"🔍 ANALYSE DE SIMILARITÉ")
        print(f"{'='*70}")
        print(f"\n📊 Compétence 1: {result['competence1']}")
        print(f"   └─ Nombre de métiers: {result['nb_metiers_comp1']}")
        
        print(f"\n📊 Compétence 2: {result['competence2']}")
        print(f"   └─ Nombre de métiers: {result['nb_metiers_comp2']}")
        
        print(f"\n🔗 Métiers en commun: {result['nb_intersection']}")
        print(f"🌐 Total métiers distincts: {result['nb_union']}")
        
        print(f"\n{'='*70}")
        print(f"📈 SIMILARITÉ DE JACCARD: {result['similarite_jaccard']:.4f}")
        print(f"   Calcul: {result['nb_intersection']} / {result['nb_union']} = {result['similarite_jaccard']:.4f}")
        print(f"{'='*70}")
        
        # Interprétation du résultat
        similarite = result['similarite_jaccard']
        if similarite >= 0.7:
            interpretation = "🟢 Très similaires - Ces compétences sont fortement liées"
        elif similarite >= 0.4:
            interpretation = "🟡 Moyennement similaires - Il y a une corrélation notable"
        elif similarite >= 0.1:
            interpretation = "🟠 Faiblement similaires - Peu de métiers en commun"
        else:
            interpretation = "🔴 Très peu similaires - Compétences distinctes"
        
        print(f"\n💡 Interprétation: {interpretation}")
        
        if result['metiers_communs']:
            print(f"\n📋 Métiers utilisant les deux compétences ({len(result['metiers_communs'])}):")
            for i, metier in enumerate(result['metiers_communs'][:10], 1):
                print(f"   {i}. {metier}")
            if len(result['metiers_communs']) > 10:
                print(f"   ... et {len(result['metiers_communs']) - 10} autre(s)")

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
    competences_input = input("Entrez vos compétences (séparées par des virgules) : ")
    
    # Séparer et nettoyer les compétences
    competences_list = [comp.strip() for comp in competences_input.split(',') if comp.strip()]
    
    if not competences_list:
        print("\n❌ Aucune compétence saisie")
        return
    
    print(f"\n🔍 Recherche de métiers pour {len(competences_list)} compétence(s)...")
    
    # Requête avec CONTAINS
    query = """
    // Pour chaque compétence entrée par l'utilisateur
    UNWIND $competences as comp_input
    
    // Trouver les compétences qui correspondent (insensible à la casse)
    MATCH (s:Skill)
    WHERE toLower(s.name) CONTAINS toLower(comp_input)
    
    // Trouver les métiers liés à ces compétences
    MATCH (metier:Occupation)
    WHERE (metier)-[:REQUIRES]->(s) OR (metier)-[:OPTIONAL_SKILL]->(s)
    
    WITH DISTINCT metier, s, comp_input
    
    // Déterminer si la compétence est requise ou optionnelle pour ce métier
    WITH metier, comp_input,
         CASE 
             WHEN (metier)-[:REQUIRES]->(s) THEN 'requise'
             ELSE 'optionnelle'
         END as type_competence
    
    WITH metier,
         collect(DISTINCT CASE WHEN type_competence = 'requise' THEN comp_input END) as comps_requises_matched,
         collect(DISTINCT CASE WHEN type_competence = 'optionnelle' THEN comp_input END) as comps_opt_matched
    
    // Nettoyer les null
    WITH metier,
         [c IN comps_requises_matched WHERE c IS NOT NULL] as comps_req_match,
         [c IN comps_opt_matched WHERE c IS NOT NULL] as comps_opt_match
    
    // Récupérer toutes les compétences du métier
    OPTIONAL MATCH (metier)-[:REQUIRES]->(skill_req:Skill)
    OPTIONAL MATCH (metier)-[:OPTIONAL_SKILL]->(skill_opt:Skill)
    
    WITH metier,
         size(comps_req_match) as nb_matches_requises,
         size(comps_opt_match) as nb_matches_optionnelles,
         collect(DISTINCT skill_req.name) as comp_requises,
         collect(DISTINCT skill_opt.name) as comp_optionnelles
    
    // Filtrer les null
    WITH metier, nb_matches_requises, nb_matches_optionnelles,
         [c IN comp_requises WHERE c IS NOT NULL] as comp_req_clean,
         [c IN comp_optionnelles WHERE c IS NOT NULL] as comp_opt_clean
    
    // Calculer les statistiques
    WITH metier,
         nb_matches_requises,
         nb_matches_optionnelles,
         comp_req_clean as comp_requises,
         comp_opt_clean as comp_optionnelles,
         size(comp_req_clean) as nb_comp_requises,
         size(comp_opt_clean) as nb_comp_optionnelles,
         size(comp_req_clean) + size(comp_opt_clean) as nb_total_comp
    
    WHERE nb_matches_requises > 0 OR nb_matches_optionnelles > 0
    
    // Calculer les scores
    WITH metier, nb_matches_requises, nb_matches_optionnelles,
         comp_requises, comp_optionnelles,
         nb_comp_requises, nb_comp_optionnelles, nb_total_comp,
         CASE 
             WHEN nb_comp_requises > 0 
             THEN toFloat(nb_matches_requises) / toFloat(nb_comp_requises)
             ELSE 0.0
         END as score_requises,
         CASE 
             WHEN nb_comp_optionnelles > 0 
             THEN toFloat(nb_matches_optionnelles) / toFloat(nb_comp_optionnelles)
             ELSE 0.0
         END as score_optionnelles,
         CASE 
             WHEN nb_total_comp > 0 
             THEN toFloat(nb_matches_requises + nb_matches_optionnelles) / toFloat(nb_total_comp)
             ELSE 0.0
         END as score_global
    
    RETURN metier.occupation as metier,
           metier.code as code,
           nb_matches_requises as competences_requises_correspondantes,
           nb_matches_optionnelles as competences_optionnelles_correspondantes,
           nb_comp_requises as total_competences_requises,
           nb_comp_optionnelles as total_competences_optionnelles,
           nb_total_comp as total_competences,
           score_requises,
           score_optionnelles,
           score_global,
           comp_requises[0..5] as comp_requises,
           comp_optionnelles[0..5] as comp_optionnelles
    ORDER BY score_global DESC, nb_matches_requises DESC, nb_matches_optionnelles DESC
    LIMIT 20
    """
    
    resultats = graph.run(query, competences=competences_list).data()
    
    if not resultats:
        print(f"\n❌ Aucun métier trouvé correspondant à ces compétences")
        return
    
    # Affichage des résultats
    print(f"\n{'='*80}")
    print(f"🎯 MÉTIERS RECOMMANDÉS ({len(resultats)} résultat(s))")
    print(f"{'='*80}")
    
    for i, metier_info in enumerate(resultats, 1):
        score_req_pct = metier_info['score_requises'] * 100
        score_opt_pct = metier_info['score_optionnelles'] * 100
        score_global_pct = metier_info['score_global'] * 100
        
        # Déterminer le niveau de correspondance global
        if score_global_pct >= 80:
            badge = "🟢 EXCELLENT"
        elif score_global_pct >= 60:
            badge = "🟡 TRÈS BON"
        elif score_global_pct >= 40:
            badge = "🟠 BON"
        else:
            badge = "🔵 PARTIEL"
        
        print(f"\n{i}. 📋 {metier_info['metier']}")
        print(f"   Code: {metier_info['code']}")
        print(f"   {badge} - Score global: {score_global_pct:.1f}%")
        print(f"   ✅ Compétences requises: {metier_info['competences_requises_correspondantes']}/{metier_info['total_competences_requises']} ({score_req_pct:.1f}%)")
        print(f"   ⭐ Compétences optionnelles: {metier_info['competences_optionnelles_correspondantes']}/{metier_info['total_competences_optionnelles']} ({score_opt_pct:.1f}%)")
        print(f"   📊 Total: {metier_info['competences_requises_correspondantes'] + metier_info['competences_optionnelles_correspondantes']}/{metier_info['total_competences']}")
        
        # Afficher quelques compétences requises
        if metier_info['comp_requises'] and metier_info['comp_requises'][0]:
            comp_a_afficher = [c for c in metier_info['comp_requises'] if c]
            if comp_a_afficher:
                print(f"   🔹 Compétences requises (exemples): {', '.join(comp_a_afficher[:3])}")
                if len(comp_a_afficher) > 3:
                    print(f"      ... et {len(comp_a_afficher) - 3} autre(s)")
        
        # Afficher quelques compétences optionnelles
        if metier_info['comp_optionnelles'] and metier_info['comp_optionnelles'][0]:
            comp_opt_afficher = [c for c in metier_info['comp_optionnelles'] if c]
            if comp_opt_afficher:
                print(f"   ⚪ Compétences optionnelles (exemples): {', '.join(comp_opt_afficher[:3])}")
                if len(comp_opt_afficher) > 3:
                    print(f"      ... et {len(comp_opt_afficher) - 3} autre(s)")
    
    print(f"\n{'='*80}")
    print(f"💡 Astuce: Consultez la 'Fiche métier' pour plus de détails sur un métier")
    print(f"{'='*80}")

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