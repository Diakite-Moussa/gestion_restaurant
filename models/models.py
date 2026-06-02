# from odoo import models, fields, api


# class gestion_restaurant(models.Model):
#     _name = 'gestion_restaurant.gestion_restaurant'
#     _description = 'gestion_restaurant.gestion_restaurant'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

