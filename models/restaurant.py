from odoo import models, fields, api

class RestaurantTable(models.Model):
    _name = 'gestion.table'
    _description = 'Table du restaurant'

    name = fields.Char(string='Numéro de table', required=True)
    capacite = fields.Integer(string='Capacité', required=True)
    etat = fields.Selection([
        ('libre', 'Libre'),
        ('occupee', 'Occupée'),
        ('reservee', 'Réservée'),
    ], string='État', default='libre')

class Plat(models.Model):
    _name = 'gestion.plat'
    _description = 'Plat du restaurant'

    name = fields.Char(string='Nom du plat', required=True)
    prix = fields.Float(string='Prix', required=True)
    categorie = fields.Selection([
        ('entree', 'Entrée'),
        ('plat_principal', 'Plat principal'),
        ('dessert', 'Dessert'),
        ('boisson', 'Boisson'),
    ], string='Catégorie', required=True)
    description = fields.Text(string='Description')
    disponible = fields.Boolean(string='Disponible', default=True)
    product_id = fields.Many2one('product.product', string='Produit lié (Inventaire)')

class LigneCommande(models.Model):
    _name = 'gestion.ligne.commande'
    _description = 'Ligne de commande'

    commande_id = fields.Many2one('gestion.commande', string='Commande', required=True)
    plat_id = fields.Many2one('gestion.plat', string='Plat', required=True)
    quantite = fields.Integer(string='Quantité', default=1)
    prix_unitaire = fields.Float(string='Prix unitaire', related='plat_id.prix', store=True)
    sous_total = fields.Float(string='Sous-total', compute='_compute_sous_total', store=True)

    @api.depends('quantite', 'prix_unitaire')
    def _compute_sous_total(self):
        for line in self:
            line.sous_total = line.quantite * line.prix_unitaire

class RestaurantCommande(models.Model):
    _name = 'gestion.commande'
    _description = 'Commande du restaurant'

    name = fields.Char(string='Numéro de commande', required=True)
    table_id = fields.Many2one('gestion.table', string='Table', required=True)
    date_commande = fields.Datetime(string='Date de commande', default=fields.Datetime.now)
    etat = fields.Selection([
        ('en_attente', 'En attente'),
        ('en_preparation', 'En préparation'),
        ('servie', 'Servie'),
        ('payee', 'Payée'),
    ], string='État', default='en_attente')
    ligne_ids = fields.One2many('gestion.ligne.commande', 'commande_id', string='Lignes de commande')
    montant_total = fields.Float(string='Montant total', compute='_compute_montant_total', store=True)

    @api.depends('ligne_ids.sous_total')
    def _compute_montant_total(self):
        for commande in self:
            commande.montant_total = sum(commande.ligne_ids.mapped('sous_total'))

    def action_en_preparation(self):
        self.etat = 'en_preparation'

    def action_servie(self):
        self.etat = 'servie'

    def action_payee(self):
        self.etat = 'payee'
