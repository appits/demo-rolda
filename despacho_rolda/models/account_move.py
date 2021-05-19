from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    despacho_id = fields.Many2one('despacho.despacho', 'Despacho')
    total_qty = fields.Float('Cantidad total', digits='Product Unit of Measure', compute='_compute_total_qty')
    total_weight = fields.Float('Kg', digits='Product Unit of Measure', compute='_compute_total_qty')
    partner_city = fields.Char('Ciudad', related='partner_id.city')

    @api.depends('invoice_line_ids')
    def _compute_total_qty(self):
        for record in self:
            record.total_qty = sum(record.invoice_line_ids.mapped('quantity'))
            record.total_weight = sum(record.invoice_line_ids.mapped('product_id.weight'))
