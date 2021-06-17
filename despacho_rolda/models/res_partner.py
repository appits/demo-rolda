from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_transport = fields.Boolean('Es compañía de transporte', default=False)
    vehicle_license_plate = fields.Char('Vehículo / Placa')
