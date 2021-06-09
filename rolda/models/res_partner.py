from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    nit = fields.Char('NIT')
    sale_zone = fields.Text('Zona de venta')
    segment = fields.Text('Segmento')
    salesman_code = fields.Char('Cod. Vendedor', size=10)
    nielsen_code = fields.Integer('Cod. Nielsen')
    nielsen = fields.Char('Nielsen', size=100)
    code_state = fields.Char('Cod. estado', related='state_id.ubigeo')
    code_municipality = fields.Char('Cod. Municipio', related='municipality_id.ubigeo')
    code_parish = fields.Char('Cod. parroquia', related='parish_id.ubigeo')


