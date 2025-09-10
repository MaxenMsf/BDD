-- Type de domaine
CREATE DOMAIN genre_type AS CHAR(1) CHECK (VALUE IN ('M', 'F'));
CREATE DOMAIN code_postal_type AS CHAR(5) CHECK (VALUE ~ '^[0-9]{5}$');
CREATE DOMAIN telephone_type AS VARCHAR(15) CHECK (VALUE ~ '^[0-9\-\+\s\.]+$');
CREATE DOMAIN prix_type AS DECIMAL(10,2) CHECK (VALUE > 0);
CREATE DOMAIN stock_type AS INTEGER CHECK (VALUE >= 0);
CREATE DOMAIN quantite_type AS INTEGER CHECK (VALUE > 0);

-- Type composite pour adresse
CREATE TYPE adresse_type AS (
    num INTEGER,
    rue TEXT,
    cp code_postal_type,
    ville TEXT
);

-- Table client utilisant les types
CREATE TABLE client (
    num SERIAL PRIMARY KEY,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    dateNaissance DATE,
    telephone telephone_type,
    genre genre_type,
    adresse adresse_type
);

-- Table usine
CREATE TABLE usine (
    num SERIAL PRIMARY KEY,
    nomU TEXT NOT NULL,
    adresse adresse_type
);

-- Table produit
CREATE TABLE produit (
    num SERIAL PRIMARY KEY,
    designation TEXT NOT NULL,
    prix prix_type NOT NULL,
    stock stock_type DEFAULT 0,
    usine_num INTEGER REFERENCES usine(num)
);

-- Table facture
CREATE TABLE facture (
    num SERIAL PRIMARY KEY,
    qte quantite_type NOT NULL,
    client_num INTEGER REFERENCES client(num),
    produit_num INTEGER REFERENCES produit(num)
);

-- Insertion d'usines
INSERT INTO usine (nomU, adresse) VALUES
('Usine Nord', ROW(10, 'Zone Industrielle Nord', '59000', 'Lille')),
('Usine Sud', ROW(25, 'Zone Industrielle Sud', '13000', 'Marseille')),
('Usine Est', ROW(5, 'Parc Technologique Est', '67000', 'Strasbourg')),
('Usine Ouest', ROW(18, 'Zone Artisanale Ouest', '35000', 'Rennes'));

-- Insertion de clients fictifs
INSERT INTO client (nom, prenom, dateNaissance, telephone, genre, adresse) VALUES
('Dupont', 'Jean', '1985-03-15', '0123456789', 'M', ROW(123, 'Rue de la Paix', '75001', 'Paris')),
('Martin', 'Marie', '1990-07-22', '0456789012', 'F', ROW(45, 'Avenue des Champs', '69000', 'Lyon')),
('Bernard', 'Pierre', '1982-11-08', '0491234567', 'M', ROW(67, 'Boulevard Victor Hugo', '13000', 'Marseille')),
('Dubois', 'Sophie', '1988-05-12', '0534567890', 'F', ROW(89, 'Rue de la République', '31000', 'Toulouse')),
('Moreau', 'Luc', '1975-09-30', '0556789012', 'M', ROW(12, 'Place du Marché', '33000', 'Bordeaux')),
('Leroy', 'Claire', '1992-01-18', '0145678901', 'F', ROW(78, 'Rue Nationale', '59000', 'Lille')),
('Roux', 'Michel', '1980-12-03', '0387654321', 'M', ROW(56, 'Avenue de la Liberté', '67000', 'Strasbourg')),
('Fournier', 'Anne', '1987-04-25', '0298765432', 'F', ROW(34, 'Rue du Commerce', '35000', 'Rennes')),
('Girard', 'Paul', '1983-08-14', '0478901234', 'M', ROW(90, 'Boulevard de la Gare', '69000', 'Lyon')),
('Bonnet', 'Isabelle', '1991-06-07', '0156789012', 'F', ROW(23, 'Place de la Mairie', '75001', 'Paris'));

-- Insertion de produits
INSERT INTO produit (designation, prix, stock, usine_num) VALUES
('Ordinateur Portable', 899.99, 50, 1),
('Smartphone', 599.99, 100, 1),
('Tablette', 399.99, 75, 2),
('Casque Audio', 149.99, 200, 2),
('Clavier Mécanique', 89.99, 150, 3),
('Souris Gaming', 59.99, 300, 3),
('Écran 24 pouces', 299.99, 80, 4),
('Webcam HD', 79.99, 120, 4),
('Disque SSD 1To', 129.99, 90, 1),
('Chargeur USB-C', 29.99, 500, 2);

-- Insertion de factures
INSERT INTO facture (qte, client_num, produit_num) VALUES
(1, 1, 1),    -- Jean Dupont achète 1 ordinateur portable
(2, 2, 2),    -- Marie Martin achète 2 smartphones
(1, 3, 3),    -- Pierre Bernard achète 1 tablette
(3, 4, 4),    -- Sophie Dubois achète 3 casques audio
(1, 5, 5),    -- Luc Moreau achète 1 clavier mécanique
(2, 6, 6),    -- Claire Leroy achète 2 souris gaming
(1, 7, 7),    -- Michel Roux achète 1 écran 24 pouces
(1, 8, 8),    -- Anne Fournier achète 1 webcam HD
(2, 9, 9),    -- Paul Girard achète 2 disques SSD
(5, 10, 10);  -- Isabelle Bonnet achète 5 chargeurs USB-C

-- 3. Modifier une adresse d'un client particulier
UPDATE client 
SET adresse = ROW(456, 'Nouvelle Rue de la Liberté', '75002', 'Paris')
WHERE nom = 'Dupont' AND prenom = 'Jean';

-- 4. Ajouter un attribut Ntéléphones (liste des numéros de téléphone)
ALTER TABLE client ADD COLUMN Ntelephones telephone_type[];
UPDATE client SET Ntelephones = ARRAY[telephone];

-- 5. Afficher le nom, prénom et premier numéro de téléphone de chaque client
SELECT nom, prenom, Ntelephones[1] AS premier_telephone
FROM client;

-- 7. Ajouter un numéro de téléphone à un client spécifique
UPDATE client 
SET Ntelephones = array_append(Ntelephones, '0987654321')
WHERE nom = 'Dupont' AND prenom = 'Jean';

-- 8. Supprimer un numéro de téléphone à un client spécifique
UPDATE client 
SET Ntelephones = array_remove(Ntelephones, '0987654321')
WHERE nom = 'Dupont' AND prenom = 'Jean';

-- 9. Modifier le schéma de la table facture
-- D'abord, créer un type composite pour les produits commandés
CREATE TYPE produit_commande_type AS (
    produit_num INTEGER,
    qte quantite_type
);

-- Supprimer l'ancienne table facture
DROP TABLE facture;

-- Créer la nouvelle table facture
CREATE TABLE facture (
    num SERIAL PRIMARY KEY,
    client_num INTEGER REFERENCES client(num),
    produits_commandes produit_commande_type[]
);

-- 10. Ajouter des factures fictives selon la nouvelle structure
INSERT INTO facture (client_num, produits_commandes) VALUES
(1, ARRAY[ROW(1, 1), ROW(9, 1)]::produit_commande_type[]),  -- Jean Dupont: 1 ordinateur + 1 SSD
(2, ARRAY[ROW(2, 2), ROW(4, 1)]::produit_commande_type[]),  -- Marie Martin: 2 smartphones + 1 casque
(3, ARRAY[ROW(3, 1)]::produit_commande_type[]),             -- Pierre Bernard: 1 tablette
(4, ARRAY[ROW(4, 3), ROW(6, 2)]::produit_commande_type[]),  -- Sophie Dubois: 3 casques + 2 souris
(5, ARRAY[ROW(5, 1), ROW(7, 1)]::produit_commande_type[]);  -- Luc Moreau: 1 clavier + 1 écran

-- 11. Modifier la quantité commandée d'un produit spécifique dans une facture
-- Exemple: modifier la quantité du produit 1 dans la facture 1
UPDATE facture 
SET produits_commandes = array_replace(
    produits_commandes,
    ROW(1, 1)::produit_commande_type,
    ROW(1, 2)::produit_commande_type
)
WHERE num = 1;

-- 12. Clients ayant commandé des produits fabriqués dans leur ville
SELECT DISTINCT c.nom, c.prenom, (c.adresse).ville as ville_client
FROM client c
JOIN facture f ON c.num = f.client_num,
unnest(f.produits_commandes) as pc(produit_num, qte)
JOIN produit p ON pc.produit_num = p.num
JOIN usine u ON p.usine_num = u.num
WHERE (c.adresse).ville = (u.adresse).ville;

-- 13. Nombre de produits commandés par ville d'usine
SELECT (u.adresse).ville as ville_usine, 
       SUM(pc.qte) as total_produits_commandes
FROM facture f,
unnest(f.produits_commandes) as pc(produit_num, qte)
JOIN produit p ON pc.produit_num = p.num
JOIN usine u ON p.usine_num = u.num
GROUP BY (u.adresse).ville
ORDER BY total_produits_commandes DESC;