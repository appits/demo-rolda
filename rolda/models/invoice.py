from odoo import models, fields


class account_invoice(orm.Model):
    _inherit = 'account.move'

    address_shipping_id = fields.many2one(
            'res.partner',
            'Shipping Address',
            help="Delivery address for current invoice.")