# Gestion Restaurant — Module Odoo 17

Module personnalisé Odoo 17 pour la gestion d'un restaurant.

## Auteur

Moussa Diakite — Étudiant en Génie Informatique, Université Mundiapolis, Casablanca

## GitHub

https://github.com/Diakite-Moussa/gestion_restaurant

## Fonctionnalités

- Gestion des Tables avec séquence automatique (Liste, Formulaire, Kanban)
- Gestion des Réservations avec workflow (En attente / Confirmée / Annulée)
- Gestion des Plats avec lien Inventaire (Liste, Formulaire, Kanban)
- Gestion des Commandes avec lignes de commande et calcul automatique
- Workflow commandes : En attente > En préparation > Servie > Payée
- Synchronisation état table lors des transitions de commande
- Vues Graph et Pivot sur les commandes
- Rapport PDF QWeb avec détail des lignes
- Contraintes de validation métier (capacité, nombre de personnes, quantité)

## Modèles

- gestion.table : Tables du restaurant
- gestion.plat : Plats du menu
- gestion.reservation : Réservations de tables
- gestion.ligne.commande : Lignes de commande
- gestion.commande : Commandes

## Dépendances

- base
- sale_management
- purchase
- stock

## Installation

1. Copier le dossier dans le répertoire addons Odoo
2. Ajouter le chemin dans odoo.conf (addons_path)
3. Redémarrer Odoo et installer le module depuis le menu Applications

## Licence

LGPL-3
