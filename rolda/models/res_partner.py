from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    nit = fields.Char('NIT')
    sale_zone = fields.Text('Zona de venta')
    segment = fields.Text('Segmento')
    salesman_code = fields.Char('Cod. Vendedor', size=10)
    nielsen_code = fields.Integer('Cod. Nielsen')
    nielsen = fields.Char('Nielsen', size=100)
