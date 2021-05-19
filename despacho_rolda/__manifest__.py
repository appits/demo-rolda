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
        'wizard/print_guide_views.xml',
        'views/assets.xml',
        'views/despacho_views.xml',
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
        'report/report_despacho_templates.xml',
        'report/despacho_rolda_reports.xml',
    ],
    'installable': True,
}
