Gestionnaire de dépenses

Une application de gestion de dépenses personnelles développée en Python avec CustomTkinter et SQLite.

Installation

```bash
pip install customtkinter pandas matplotlib tkcalendar
python expense-manager.py
```

Fonctionnalités

- Ajouter une dépense avec un montant, une catégorie et une date
- Afficher la liste de toutes les dépenses enregistrées
- Supprimer une dépense par son ID
- Charger une dépense existante dans les champs pour la modifier
- Analyses automatiques : total, montant maximum, minimum et nombre de dépenses
- Graphique des dépenses par catégorie avec plusieurs types d'affichage

Comment utiliser

**Ajouter une dépense**
Remplis les champs montant, catégorie et date puis clique sur "Ajouter la dépense".

**Supprimer une dépense**
Entre l'ID de la dépense dans le champ ID puis clique sur "Supprimer".

**Modifier une dépense**
Entre l'ID dans le champ ID, clique sur "Charger" pour remplir les champs automatiquement, modifie ce que tu veux puis clique sur "Modifier".

**Changer le graphique**
Clique sur le bouton "Graphique" pour passer d'un type à l'autre (barres, camembert, courbe, barres horizontales).

Technologies utilisées

- Python 3
- CustomTkinter — interface graphique
- SQLite — base de données
- Pandas — analyses des données
- Matplotlib — graphiques
- Tkcalendar — sélecteur de date

Auteur

SamiraK-yeray
