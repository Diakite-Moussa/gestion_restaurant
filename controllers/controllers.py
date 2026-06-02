# from odoo import http


# class GestionRestaurant(http.Controller):
#     @http.route('/gestion_restaurant/gestion_restaurant', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_restaurant/gestion_restaurant/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_restaurant.listing', {
#             'root': '/gestion_restaurant/gestion_restaurant',
#             'objects': http.request.env['gestion_restaurant.gestion_restaurant'].search([]),
#         })

#     @http.route('/gestion_restaurant/gestion_restaurant/objects/<model("gestion_restaurant.gestion_restaurant"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_restaurant.object', {
#             'object': obj
#         })

