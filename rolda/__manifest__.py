{
    'name': 'Rolda',
    'version': '13.0.0.0.1',
    'depends': ['locv_fiscal_book', 'locv_withholding_iva', 'locv_account_fiscal_requirements'],
    'author': 'Keiver Peña',
    'license': 'AGPL-3',
    'website': 'https://gitlab.com/keiverobles',
    'category': 'Libros Fiscales-Accounting',
    'data': [
        'data/company_data.xml',
        'views/assets.xml',
        'views/res_partner_views.xml',
        #'wizard/export_bank_payments_views.xml',
        'report/rolda_reports.xml',
        'report/fiscal_purchase_book_report.xml',
        'report/fiscal_book_report.xml',
        'report/report_invoice.xml',
        'report/withholding_vat_report.xml',
    ],
    'installable': True,
}
