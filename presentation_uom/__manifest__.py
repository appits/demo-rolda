# -*- coding: utf-8 -*-
{
    'name': "presentation_uom",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Luis Auyadermont",

    'category': 'product',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product.xml',
        'views/stock_move.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # ~ 'demo/demo.xml',
    ],
}
