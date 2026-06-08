from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RestaurantTable(models.Model):
    _name = 'gestion.table'
    _description = 'Table du restaurant'
    _order = 'name'

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Ce numéro de table existe déjà.')
    ]

    name = fields.Char(string='Numéro de table', required=True, copy=False, readonly=True, default='/')
    capacite = fields.Integer(string='Capacité', required=True)
    etat = fields.Selection([
        ('libre', 'Libre'),
        ('occupee', 'Occupée'),
        ('reservee', 'Réservée'),
    ], string='État', default='libre')

    @api.constrains('capacite')
    def _check_capacite(self):
        for table in self:
            if table.capacite <= 0:
                raise ValidationError("La capacité de la table doit être supérieure à 0.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('gestion.table') or '/'
        return super().create(vals_list)


class Plat(models.Model):
    _name = 'gestion.plat'
    _description = 'Plat du restaurant'
    _order = 'categorie, name'

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

    @api.constrains('prix')
    def _check_prix(self):
        for plat in self:
            if plat.prix <= 0:
                raise ValidationError("Le prix du plat doit être supérieur à 0.")


class Reservation(models.Model):
    _name = 'gestion.reservation'
    _description = 'Réservation de table'
    _order = 'date_reservation desc'

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True, default='/')
    client_name = fields.Char(string='Nom du client', required=True)
    table_id = fields.Many2one('gestion.table', string='Table', required=True)
    date_reservation = fields.Datetime(string='Date de réservation', required=True)
    nombre_personnes = fields.Integer(string='Nombre de personnes')
    etat = fields.Selection([
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée'),
    ], string='État', default='en_attente')

    @api.constrains('nombre_personnes', 'table_id')
    def _check_nombre_personnes(self):
        for res in self:
            if res.nombre_personnes <= 0:
                raise ValidationError("Le nombre de personnes doit être supérieur à 0.")
            if res.table_id and res.nombre_personnes > res.table_id.capacite:
                raise ValidationError(
                    f"Le nombre de personnes ({res.nombre_personnes}) dépasse "
                    f"la capacité de la table ({res.table_id.capacite})."
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('gestion.reservation') or '/'
        return super().create(vals_list)

    def action_confirmer(self):
        self.etat = 'confirmee'
        self.table_id.etat = 'reservee'

    def action_annuler(self):
        self.etat = 'annulee'
        self.table_id.etat = 'libre'


class LigneCommande(models.Model):
    _name = 'gestion.ligne.commande'
    _description = 'Ligne de commande'

    commande_id = fields.Many2one('gestion.commande', string='Commande', required=True)
    plat_id = fields.Many2one('gestion.plat', string='Plat', required=True)
    quantite = fields.Integer(string='Quantité', default=1)
    prix_unitaire = fields.Float(string='Prix unitaire', related='plat_id.prix', store=True)
    sous_total = fields.Float(string='Sous-total', compute='_compute_sous_total', store=True)

    @api.constrains('quantite')
    def _check_quantite(self):
        for line in self:
            if line.quantite <= 0:
                raise ValidationError("La quantité doit être supérieure à 0.")

    @api.depends('quantite', 'prix_unitaire')
    def _compute_sous_total(self):
        for line in self:
            line.sous_total = line.quantite * line.prix_unitaire


class RestaurantCommande(models.Model):
    _name = 'gestion.commande'
    _description = 'Commande du restaurant'
    _order = 'date_commande desc'

    name = fields.Char(string='Numéro de commande', required=True, copy=False, readonly=True, default='/')
    table_id = fields.Many2one('gestion.table', string='Table', required=True)
    serveur_id = fields.Many2one('res.users', string='Serveur')
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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('gestion.commande') or '/'
        return super().create(vals_list)

    def action_en_preparation(self):
        self.etat = 'en_preparation'
        self.table_id.etat = 'occupee'

    def action_servie(self):
        self.etat = 'servie'

    def action_payee(self):
        self.etat = 'payee'
        self.table_id.etat = 'libre'
