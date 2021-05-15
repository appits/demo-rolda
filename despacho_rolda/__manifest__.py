{
    'name': 'Despacho Rolda',
    'version': '13.0.0.0.1',
    'depends': ['rolda', 'stock', 'account'],
    'author': 'Keiver Peña',
    'license': 'AGPL-3',
    'website': 'https://gitlab.com/keiverobles',
    'category': 'Libros Fiscales-Accounting',
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/despacho_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
}
