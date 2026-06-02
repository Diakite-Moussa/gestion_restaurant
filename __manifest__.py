{
    'name': 'Gestion de Restaurant',
    'version': '1.0',
    'category': 'Restaurant',
    'summary': 'Module de gestion de restaurant',
    'author': 'Moussa Diakite',
    'website': 'https://www.example.com',
    'license': 'LGPL-3',
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/restaurant_view.xml',
        'reports/commande_report.xml',
    ],
    'installable': True,
    'application': True,
}
