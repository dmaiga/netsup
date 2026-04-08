# NETSUP – Système de contrôle des sites

## Documentation V1.1

## 1. Présentation du projet

Ce projet consiste à développer une **application web permettant de contrôler et suivre les sites d’intervention de l’entreprise NETSUP**, spécialisée dans les services de nettoyage et d’entretien.

L'application permet désormais aux superviseurs de :

* enregistrer leurs visites sur les sites
* vérifier la présence des techniciens (pointage individuel)
* évaluer la qualité du nettoyage
* signaler les problèmes observés
* fournir des preuves (photos, GPS)
* générer des rapports détaillés pour chaque site

Les données collectées sont centralisées dans une base de données et accessibles via un **tableau de bord administratif** permettant d’analyser la performance des sites et l’activité des superviseurs.

---

## 2. Contexte métier

NETSUP gère :

- plusieurs **techniciens de surface**  
- répartis sur **plus de 200 sites**  
- encadrés par **des superviseurs**  

---

### Organisation opérationnelle

- Chaque **superviseur est responsable d’un ensemble de sites**  
- Les techniciens sont **affectés aux sites** via une gestion d’affectation  
- Un technicien peut intervenir sur **un ou plusieurs sites**  
- Les superviseurs assurent le **suivi et le contrôle des équipes sur le terrain**  

---

### Fonctionnement terrain

Chaque site dispose :

- d’une **fiche de présence papier**  
- d’un **effectif prévu de techniciens**  

Les superviseurs effectuent des **visites de contrôle** pour :

- vérifier la présence réelle des techniciens  
- contrôler la qualité du travail effectué  
- identifier les incidents ou anomalies  
- documenter les observations terrain  

---

### Limites du fonctionnement actuel

Avant la mise en place de la solution :

- les contrôles sont **majoritairement manuels**  
- les données sont **éparpillées ou non structurées**  
- il est difficile de :
  - suivre la couverture des sites  
  - analyser les absences des techniciens  
  - détecter les anomalies récurrentes  
  - produire des rapports fiables pour la direction  

---

### Objectif du projet

Le projet NETSUP vise à :

- **numériser les contrôles terrain**  
- **centraliser les données opérationnelles**  
- permettre un **suivi en temps réel des sites et des équipes**  
- améliorer la **qualité des prestations**  
- fournir des **indicateurs fiables pour la prise de décision**  

 Cette première version (V1) est centrée sur le **contrôle des sites**, avec une évolution prévue vers une **gestion RH complète (V2)**.

---

## 3. Objectifs de la V1.1 (mis à jour)

La version 1.1 du système permet :

1. enregistrer les visites des superviseurs sur les sites  
2. effectuer un **pointage individuel des techniciens** (présence, absence, motif)  
3. calculer les indicateurs de présence (présents, absents, taux)  
4. évaluer la qualité du site  
5. enregistrer et suivre les incidents (avec statut de résolution)  
6. documenter les problèmes observés et les observations terrain  
7. stocker des preuves (photos, GPS)  
8. suivre les visites par site et vérifier le respect des quotas (minimum 2 visites/semaine)  
9. afficher un tableau de bord administratif (couverture, incidents, qualité, présence)  
10. générer et consulter des rapports détaillés par site, superviseur ou période  

---

## 4. Utilisateurs du système

### Superviseurs

Les superviseurs sont les principaux utilisateurs opérationnels du système.  
Ils sont responsables du suivi des sites qui leur sont assignés.

Ils utilisent l’application pour :

- accéder aux sites sous leur responsabilité  
- effectuer les contrôles terrain  
- renseigner le formulaire de contrôle  
- réaliser le pointage des techniciens (présence, absence, motif)  
- signaler les incidents et problèmes observés  
- ajouter des observations et des preuves (photos)  
- consulter l’historique des visites  

---

### Administration / RH

L’administration utilise le système pour le pilotage et le suivi global.

Elle peut :

- consulter l’ensemble des contrôles effectués  
- suivre la couverture des sites (visites réalisées vs attendues)  
- analyser les présences et absences  
- suivre les incidents et leur résolution  
- gérer les sites et les affectations des techniciens  

---

### Direction

La direction utilise le système comme outil d’aide à la décision.

Elle peut :

- suivre la performance globale des sites  
- identifier les sites critiques ou non conformes  
- analyser les tendances (présence, qualité, incidents)  
- exploiter les rapports pour orienter les décisions stratégiques  

---

## 5. Fonctionnalités principales

### Visites obligatoires

Chaque site doit être contrôlé :

**au minimum deux fois par semaine**

---

### Objectif de supervision

Le système permet de vérifier :

- quels sites ont été contrôlés  
- quels sites n'ont pas encore été visités  
- combien de visites chaque superviseur a effectué  

---

### Pointage des techniciens

Le système intègre un **pointage individuel des techniciens** lors de chaque contrôle.

Pour chaque visite, le superviseur peut :

- enregistrer la présence ou l’absence de chaque technicien  
- préciser un motif en cas d’absence (retard, congé, maladie, etc.)  
- ajouter un commentaire si nécessaire  

À partir de ces données, le système permet de :

- calculer le nombre de techniciens présents et absents  
- déterminer le taux de présence par site  
- analyser les absences sur une période donnée  
- identifier les agents avec des absences récurrentes  

---

## 6. Fonctionnement du système

### Étape 1 : accès au site

Le superviseur accède au site à contrôler via l’application :

- sélection du site depuis son espace  
- ou identification rapide du site (ex : QR code)  

---

### Étape 2 : vérification terrain

Le superviseur réalise les vérifications sur place :

- état général du site  
- conformité du travail effectué  
- fiche de présence des techniciens  

---

### Étape 3 : pointage et saisie du contrôle

Le superviseur saisit les informations dans l’application :

- pointage individuel des techniciens (présence / absence / motif)  
- évaluation de la qualité du site  
- signalement des incidents ou problèmes  
- ajout d’observations  

---

### Étape 4 : ajout des preuves

Le superviseur peut compléter le contrôle avec :

- photos du site  
- photo de la fiche de présence  
- données de localisation (GPS si disponible)  

---

### Étape 5 : enregistrement et exploitation

Une fois validé :

- le contrôle est enregistré dans le système  
- les données sont immédiatement disponibles dans le tableau de bord  
- les indicateurs (présence, qualité, couverture) sont mis à jour  

---

## 7. Formulaire de contrôle 

Le formulaire de contrôle permet au superviseur d’effectuer un **audit complet du site**, incluant l’évaluation de la qualité, la gestion des incidents et le pointage individuel des techniciens.

---

### 7.1 Informations générales

Les informations suivantes sont automatiquement enregistrées :

* superviseur
* site
* date du contrôle (automatique)
* coordonnées GPS (si disponibles)

---

### 7.2 Pointage des techniciens

Le système repose sur un **pointage individuel des techniciens** affectés au site.

Pour chaque technicien, le superviseur renseigne :

* statut : présent ou absent
* motif d’absence (si absent) :

  * retard
  * absent non prévenu
  * absent prévenu
  * congé
  * maladie
  * autre
* commentaire optionnel

Chaque enregistrement est sauvegardé individuellement afin de permettre un suivi précis des présences.

---

### 7.3 Indicateurs de présence

À partir des pointages individuels, le système permet de déterminer :

* le nombre de techniciens présents
* le nombre de techniciens absents
* le taux de présence (%)

Ces indicateurs permettent d’évaluer rapidement la situation du site lors du contrôle.

---

### 7.4 État du site

Le superviseur évalue la qualité globale du nettoyage :

* Très propre
* Propre
* Moyen
* Mauvais

---

### 7.5 Gestion des incidents

Le formulaire permet de signaler un incident :

* activation du statut incident (oui/non)
* description obligatoire en cas d’incident
* suivi de résolution :

  * incident résolu ou non
  * date de résolution

---

### 7.6 Problèmes observés

Un champ permet de détailler les problèmes rencontrés sur le site, tels que :

* défaut de qualité
* manque de matériel
* non-respect des consignes
* autres anomalies

---

### 7.7 Observations

Champ libre permettant d’ajouter des commentaires complémentaires sur le contrôle.

---

### 7.8 Preuves terrain

Le superviseur peut ajouter des preuves visuelles :

* photo du site
* photo de la fiche de présence

Les images peuvent être capturées directement depuis un appareil mobile afin de garantir la fiabilité des contrôles.

---

## 8. Tableau de bord administratif 

Le tableau de bord administratif permet un pilotage global de l’activité, avec un suivi en temps réel des contrôles, des incidents, de la couverture des sites et de la performance opérationnelle.

---

### 8.1 Suivi de la couverture hebdomadaire

Le système suit le respect des objectifs de contrôle :

- nombre total de contrôles effectués sur la semaine  
- nombre total de sites actifs  
- objectif hebdomadaire (minimum 2 visites par site)  
- taux de couverture global (%)  

Une vue détaillée permet d’identifier :

- les sites conformes (quota atteint)  
- les sites partiellement couverts  
- les sites non visités  

---

### 8.2 Suivi des présences 

Les indicateurs sont calculés à partir des pointages individuels :

- total des présences  
- total des absences  
- taux de présence global  
- taux de présence par site  
- taux de présence par agent  

Le système permet également d’identifier :

- les agents avec absences répétées  
- les agents à risque (faible taux de présence)  

---

### 8.3 Suivi des incidents

Le dashboard met en avant les incidents critiques :

- liste des incidents non résolus  
- nombre total d’incidents actifs  
- suivi des résolutions (date + statut)  

Les incidents peuvent être traités directement depuis l’interface.

---

### 8.4 Suivi de la qualité des sites

Le système permet d’identifier rapidement les sites problématiques :

- derniers contrôles avec mauvaise évaluation  
- sites critiques (qualité "mauvais")  
- historique des contrôles par site  

---

### 8.5 Activité des superviseurs

Suivi de la performance des superviseurs :

- nombre de contrôles réalisés  
- fréquence des visites  
- sites couverts  
- historique des passages par site  

---

### 8.6 Analyse et reporting avancé

Des vues de reporting permettent une analyse plus fine :

- rapport de présence (par agent et par site)  
- détection des anomalies (absences fréquentes)  
- comparaison des performances entre sites  
- filtrage avancé des rapports :
  - par site  
  - par superviseur  
  - par période  
  - par niveau de qualité  

---

### 8.7 Gestion opérationnelle des sites

Le dashboard permet également :

- gestion des sites (création, activation, configuration)  
- affectation des techniciens aux sites  
- suivi des effectifs réels vs prévus  


---

## 9. Livrables attendus

Le projet NETSUP est structuré en deux phases évolutives :

### V1 – Contrôle des sites (version actuelle)

La version 1 est entièrement dédiée au **contrôle opérationnel des sites**.

Elle comprend :

1. une application web de contrôle terrain  
2. un système d’identification des sites (QR code ou sélection)
3. une base de données centralisée  
4. un formulaire de contrôle avec pointage individuel des techniciens  
5. un tableau de bord administratif (couverture, incidents, qualité, présence)  
6. un système d’export et de consultation des rapports  
7. une documentation d’utilisation  

Cette version constitue une base fiable pour le suivi des opérations terrain.

---

### V2 – Gestion des ressources humaines (à venir)

La version 2 introduira une couche **RH complète**, basée sur les fondations existantes.

Elle inclura :

- gestion des profils RH des techniciens (contrat, salaire, informations administratives)  
- gestion des congés et absences  
- suivi avancé du pointage et de la présence  
- structuration des données RH exploitables  
- extension du système de reporting vers des analyses RH  

Certaines structures du modèle de données préparent déjà cette évolution.

---

## 10. Résultat attendu

La solution permet à NETSUP de :

- suivre efficacement les visites des superviseurs  
- garantir une couverture minimale des sites (2 visites/semaine)  
- contrôler la présence réelle des techniciens via un pointage individuel  
- détecter rapidement les incidents et anomalies  
- améliorer la qualité des prestations sur les sites  
- centraliser et fiabiliser les données terrain  
- fournir des indicateurs exploitables pour la direction  

---

## Conclusion

La version actuelle du système constitue une **V1 centrée sur le contrôle opérationnel des sites**, robuste et orientée terrain.

Elle pose les bases d’un système structuré permettant :

- un suivi précis des activités  
- une meilleure visibilité pour la direction  
- une standardisation des contrôles  

Cette base permettra d’évoluer vers une **V2 orientée gestion des ressources humaines**, incluant :

- gestion des techniciens (contrats, salaires, profils RH)  
- gestion des congés et absences  
- analyse avancée des performances et du taux de présence  
- reporting RH automatisé  

👉 Le projet évolue ainsi d’un outil de contrôle terrain vers une **plateforme complète de pilotage opérationnel et RH**.