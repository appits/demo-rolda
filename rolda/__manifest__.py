{
    'name': 'Rolda',
    'version': '13.0.0.0.1',
    'depends': ['locv_fiscal_book'],
    'author': 'Keiver Peña',
    'license': 'AGPL-3',
    'website': 'https://gitlab.com/keiverobles',
    'category': 'Libros Fiscales-Accounting',
    'data': [
        'views/assets.xml',
        'views/res_partner_views.xml',
        'report/rolda_reports.xml',
        'report/fiscal_purchase_book_report.xml',
        'report/fiscal_book_report.xml',
        'report/report_invoice.xml',
    ],
    'installable': True,
}
