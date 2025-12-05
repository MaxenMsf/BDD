# Exo 1
1. Créer un RDD (allData) à partir du fichier weblog.csv.
allData = sc.textFile("weblog.csv")

2. Déterminer le nombre de lignes de l’RDD créé
allData.count()

3. Créer un deuxième RDD (RDD200) à partir de l’RDD créé (allData) qui regroupe que les accès dont le code HTTP =200.
RDD200 = allData.filter(lambda l: l.split(",")[3]== "200")

4. Calculer le pourcentage de succès (code200) des requêtes HTTTP.
total = allData.count()
total200 = RDD200.count()
pourcentage = (total200 / total * 100)
print(f"{pourcentage:.2f}%")

5. Déterminer pour chaque adresse IP le nombre d’accès.
RDDAcces = allData.filter(lambda ligne: ligne.startswith("10")).map(lambda l: l.split(",")[0]).map(lambda url: (url,1)).reduceByKey(lambda x, y: x + y)

6. Déterminez le nombre d’accès à la page login.php pour chaque adresse IP.
login_lines = data.filter(lambda l: "/login.php" in l)
ip_login_counts = (login_lines
    .map(lambda l: l.split(",",1)[0].strip())
    .map(lambda ip: (ip, 1))
    .reduceByKey(lambda a, b: a + b))
