{
    'name': 'Gestion de Restaurant',
    'version': '1.0',
    'category': 'Restaurant',
    'summary': 'Module de gestion de restaurant',
    'author': 'Moussa Diakite',
    'website': 'https://www.example.com',
    'license': 'LGPL-3',
    'depends': ['base', 'sale_management', 'purchase', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/restaurant_view.xml',
        'reports/commande_report.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
