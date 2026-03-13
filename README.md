# NETSUP – Système de contrôle des sites

## Documentation V1

## 1. Présentation du projet

Ce projet consiste à développer une **application web permettant de contrôler et suivre les sites d’intervention de l’entreprise NETSUP**, spécialisée dans les services de nettoyage et d’entretien.

L'application permettra aux superviseurs de :

* enregistrer leurs visites sur les sites
* vérifier la présence des techniciens
* évaluer la qualité du nettoyage
* signaler les problèmes observés
* fournir des preuves (photos, GPS)

Les données collectées seront centralisées dans une base de données et accessibles via un **tableau de bord administratif** permettant d’analyser la performance des sites et l’activité des superviseurs.

---

# 2. Contexte métier

NETSUP gère :

* plus de **200 techniciens de surface**
* répartis sur **plus de 20 sites**
* supervisés par **2 superviseurs**

Chaque site possède :

* une **fiche de présence papier**
* les techniciens signent cette fiche à leur arrivée

Les superviseurs effectuent des **visites de contrôle terrain** afin de vérifier :

* la présence des techniciens
* la qualité du travail
* les problèmes éventuels

Actuellement ces contrôles ne sont **pas centralisés numériquement**, ce qui rend difficile :

* le suivi des sites
* l’analyse des absences
* la production de rapports

Le projet vise donc à **numériser ce processus de contrôle**.

---

# 3. Objectifs de la V1

La version 1 du système doit permettre :

1. enregistrer les visites des superviseurs sur les sites
2. vérifier la présence globale des techniciens
3. évaluer la qualité du site
4. enregistrer les problèmes observés
5. stocker des preuves (photos)
6. suivre les visites par site
7. afficher un tableau de bord simple pour l'administration

La V1 se concentre uniquement sur **le contrôle des sites**, sans gérer encore les présences individuelles des techniciens.

---

# 4. Utilisateurs du système

## Superviseurs

Utilisent l’application sur smartphone pour :

* scanner le QR code du site
* remplir le formulaire de contrôle
* ajouter photos et observations

---

## Administration / RH

Utilisent le tableau de bord pour :

* consulter les contrôles
* suivre les sites contrôlés
* analyser les absences et problèmes

---

## Direction

Consulte les rapports pour :

* suivre la performance des sites
* identifier les sites problématiques

---

# 5. Règles métier principales

## Visites obligatoires

Chaque site doit être contrôlé :

**au minimum deux fois par semaine**

Période de référence :

```text
Lundi → Samedi
```

---

## Restriction importante

Un site **ne peut pas être contrôlé deux fois le même jour**.

Exemple :

| Jour          | Visite |
| ------------- | ------ |
| Lundi         | ✔      |
| Mardi         | ✔      |
| Lundi + Lundi | ❌      |

---

## Objectif de supervision

Le système doit permettre de vérifier :

* quels sites ont été contrôlés
* quels sites n'ont pas encore été visités
* combien de visites chaque superviseur a effectué

---

# 6. Fonctionnement du système

## Étape 1 : arrivée sur le site

Le superviseur arrive sur un site et scanne le **QR code du site**.

Le QR code ouvre directement la page de contrôle du site.

---

## Étape 2 : vérification terrain

Le superviseur vérifie :

* l’état général du site
* la fiche de présence des techniciens

---

## Étape 3 : saisie du contrôle

Le superviseur remplit un formulaire dans l’application.

---

# 7. Formulaire de contrôle

Le formulaire comprend les informations suivantes.

## Informations générales

* superviseur
* site
* date (automatique)
* localisation GPS

---

## Présence des techniciens

Le superviseur indique :

```text
Techniciens prévus
Techniciens présents
Techniciens absents
```

Une **photo de la fiche de présence** peut être ajoutée.

---

## État du site

Le superviseur évalue la qualité du nettoyage :

* Très propre
* Propre
* Moyen
* Mauvais

---

## Problèmes observés

Le superviseur peut signaler :

* retard
* absence
* manque de matériel
* travail mal exécuté
* autre problème

---

## Observations

Champ texte libre pour ajouter des commentaires.

---

## Preuves

Possibilité d’ajouter :

* photos du site
* photo de la fiche de présence

---

# 8. Tableau de bord administratif

Le tableau de bord doit permettre de visualiser :

## Suivi des contrôles

* nombre total de visites
* sites contrôlés cette semaine
* sites non contrôlés

---

## Présence des techniciens

Indicateurs :

* techniciens présents
* techniciens absents
* taux de présence par site

---

## Qualité des sites

Graphiques :

* qualité moyenne des sites
* sites avec problèmes

---

## Activité des superviseurs

Indicateurs :

* nombre de visites par superviseur
* nombre de sites visités

---

# 9. Architecture technique

L'application sera développée sous forme d'une **application web**.

### Technologies utilisées

Backend

* Django

Base de données

* PostgreSQL

Interface utilisateur

* DaisyUI
* TailwindCSS

---

# 10. Architecture système

```text
Superviseur (smartphone)

        ↓

Application Web Django

        ↓

Base de données PostgreSQL

        ↓

Tableau de bord administratif
```

---

# 11. Modèle de données simplifié

## Site

Contient les informations des sites.

```
Site
id
nom
code_site
adresse
client_nom
nombre_techniciens_prevus
qr_code
latitude
longitude
actif
```

---

## Utilisateur

```
User
id
nom
prenom
role
telephone
photo
```

Roles possibles :

```
superviseur
administration
direction
```

---

## ControleSite

Représente une visite de contrôle.

```
ControleSite
id
site
superviseur
date
gps_lat
gps_long
techniciens_prevus
techniciens_presents
techniciens_absents
etat_proprete
problemes
observations
photo_site
photo_presence
```

---

# 12. Livrables attendus

Le projet devra produire :

1. application web de contrôle des sites
2. système de scan QR code
3. base de données centralisée
4. formulaire de contrôle terrain
5. tableau de bord administratif
6. système d’export des données
7. documentation d’utilisation

---

# 13. Résultat attendu

La solution doit permettre à NETSUP de :

* suivre efficacement les visites des superviseurs
* vérifier la présence des techniciens
* améliorer la qualité des sites
* centraliser les données de contrôle
* produire des rapports fiables pour la direction

---

## Conclusion

La version 1 du système vise à **digitaliser le contrôle terrain des sites** de manière simple et efficace.

Cette base permettra ensuite d’ajouter dans les versions futures :

* gestion détaillée des techniciens
* analyse avancée des absences
* scoring des sites
* rapports automatisés plus avancés.
