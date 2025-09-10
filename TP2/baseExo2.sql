DROP TABLE IF EXISTS film CASCADE;
DROP TABLE IF EXISTS categorie CASCADE;
DROP TABLE IF EXISTS production CASCADE;
DROP TABLE IF EXISTS realisateur CASCADE;
DROP TYPE IF EXISTS adresse_type CASCADE;
DROP DOMAIN IF EXISTS code_postal_type CASCADE;
-- Type de domaine (correction pour accepter les codes postaux non français)
CREATE DOMAIN code_postal_type AS VARCHAR(10) CHECK (VALUE ~ '^[0-9A-Z\s]{2,10}$');

-- Type composite pour adresse
CREATE TYPE adresse_type AS (
    num INTEGER,
    rue TEXT,
    cp code_postal_type,
    ville TEXT
);

-- Table realisateur
CREATE TABLE realisateur (
    IDRealisateur SERIAL PRIMARY KEY,
    nom TEXT NOT NULL,
    dateNaissance DATE,
    adresse adresse_type
);

-- Table production
CREATE TABLE production (
    IDProd SERIAL PRIMARY KEY,
    nationalite TEXT NOT NULL,
    adresses adresse_type[] NOT NULL
);

-- Table categorie
CREATE TABLE categorie (
    IDCategorie SERIAL PRIMARY KEY,
    libelle TEXT NOT NULL
);

-- Table film
CREATE TABLE film (
    ISAN SERIAL PRIMARY KEY,
    titre TEXT NOT NULL,
    tags TEXT NOT NULL,
    annee INTEGER NOT NULL,
    duree INTEGER NOT NULL,
    IDRealisateur INTEGER REFERENCES realisateur(IDRealisateur),
    IDProd INTEGER REFERENCES production(IDProd),
    IDCategorie INTEGER REFERENCES categorie(IDCategorie)
);

-- 2. Insertion de données fictives

-- Insertion des catégories
INSERT INTO categorie (libelle) VALUES
('Action'),
('Drame'),
('Comédie'),
('Science-Fiction'),
('Horreur'),
('Romance');

-- Insertion des réalisateurs (corrections des codes postaux)
INSERT INTO realisateur (nom, dateNaissance, adresse) VALUES
('Spielberg', '1946-12-18', ROW(100, 'Hollywood Blvd', '90028', 'Los Angeles')),
('Tarantino', '1963-03-27', ROW(250, 'Sunset Strip', '90069', 'West Hollywood')),
('Nolan', '1970-07-30', ROW(45, 'Kensington Road', 'SW7 2AR', 'London')),
('Scorsese', '1942-11-17', ROW(78, 'Little Italy', '10013', 'New York')),
('Kubrick', '1928-07-26', ROW(12, 'Central Park West', '10025', 'New York'));

-- Insertion des productions (corrections des codes postaux)
INSERT INTO production (nationalite, adresses) VALUES
('Américaine', ARRAY[
    ROW(500, 'Hollywood Studios', '90028', 'Los Angeles'),
    ROW(1200, 'Broadway', '10019', 'New York')
]::adresse_type[]),
('Française', ARRAY[
    ROW(25, 'Rue de Rivoli', '75001', 'Paris'),
    ROW(67, 'Boulevard Saint-Germain', '75006', 'Paris')
]::adresse_type[]),
('Britannique', ARRAY[
    ROW(89, 'Piccadilly Circus', 'W1J 9HP', 'London')
]::adresse_type[]);

-- Insertion des films
INSERT INTO film (titre, tags, annee, duree, IDRealisateur, IDProd, IDCategorie) VALUES
('Jurassic Park', 'dinosaures,aventure,famille', 1993, 127, 1, 1, 1),
('Pulp Fiction', 'crime,violence,dialogue', 1994, 154, 2, 1, 1),
('Inception', 'rêves,réalité,complexe', 2010, 148, 3, 3, 4),
('Goodfellas', 'mafia,crime,biographie', 1990, 146, 4, 1, 2),
('2001 Odyssey', 'espace,intelligence,artificielle', 1968, 149, 5, 3, 4);

-- 3. Afficher la liste des catégories des films dans la base
SELECT DISTINCT c.libelle as categorie
FROM categorie c
JOIN film f ON c.IDCategorie = f.IDCategorie
ORDER BY c.libelle;

-- 4. Afficher pour chaque catégorie le nombre de films
SELECT c.libelle as categorie, COUNT(f.ISAN) as nombre_films
FROM categorie c
LEFT JOIN film f ON c.IDCategorie = f.IDCategorie
GROUP BY c.IDCategorie, c.libelle
ORDER BY nombre_films DESC;

-- 6. Afficher pour chaque ville le nombre de films réalisés par des réalisateurs de cette ville
SELECT (r.adresse).ville as ville, COUNT(f.ISAN) as nombre_films
FROM realisateur r
LEFT JOIN film f ON r.IDRealisateur = f.IDRealisateur
GROUP BY (r.adresse).ville
ORDER BY nombre_films DESC;

-- 8. Fonction pour retourner l'adresse d'un réalisateur formatée (NOUVELLE VERSION)
CREATE OR REPLACE FUNCTION format_adresse_realisateur(id_real INTEGER)
RETURNS TEXT AS $$
DECLARE
    addr_num INTEGER;
    addr_rue TEXT;
    addr_ville TEXT;
BEGIN
    -- Récupérer les composants de l'adresse séparément
    SELECT (adresse).num, (adresse).rue, (adresse).ville 
    INTO addr_num, addr_rue, addr_ville
    FROM realisateur 
    WHERE IDRealisateur = id_real;
    
    -- Vérifier si le réalisateur existe
    IF NOT FOUND THEN
        RETURN 'Réalisateur non trouvé';
    END IF;
    
    -- Vérifier si l'adresse est renseignée
    IF addr_num IS NULL OR addr_rue IS NULL OR addr_ville IS NULL THEN
        RETURN 'Adresse non renseignée';
    END IF;
    
    RETURN 'Numéro de la rue : ' || addr_num || ' Rue : ' || addr_rue || ' Ville : ' || addr_ville;
END;
$$ LANGUAGE plpgsql;

-- 9. Utiliser la fonction pour afficher toutes les adresses des réalisateurs
SELECT r.nom, format_adresse_realisateur(r.IDRealisateur) as adresse_formatee
FROM realisateur r
ORDER BY r.nom;