from odoo import models, fields, api


class Despacho(models.Model):
    """ Modelo principal de despachos. """
    _name = 'despacho.despacho'
    _description = 'Despacho'

    name = fields.Char('Nombre', default='Nuevo', readonly=True)
    date = fields.Datetime('Fecha', default=fields.Datetime.now, help='Fecha en la cual se está realizando el registro de la orden de despacho.')
    # partner_id = fields.Many2one('res.partner', 'Cliente')
    transport_company_id = fields.Many2one('res.partner', 'Compañía de transporte')
    license_plate = fields.Char(related='transport_company_id.vehicle_license_plate')
    driver_id = fields.Many2one('res.partner', 'Chofer')
    vat = fields.Char(related='driver_id.identification_id', string='CI')
    assistant_id = fields.Many2one('res.partner', 'Ayudante')
    vat_assistant = fields.Char(related='assistant_id.identification_id', string='CI asistente')
    seal = fields.Char('Precinto', help='Número de precinto relativo a la orden de despacho a realizar.')
    notes = fields.Text('Observaciones')
    order_ids = fields.Many2many('sale.order', 'order_despacho_rel', 'despacho_id', 'order_id', 'Pedidos de venta')
    user_id = fields.Many2one('res.users', 'Responsable', default=lambda self: self.env.user)
    active = fields.Boolean('Activo', default=True)

    @api.model
    def create(self, vals):
        new_id = super().create(vals)
        new_id.name = self.env['ir.sequence'].next_by_code('despacho.rolda')
        return new_id
