from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    despacho_id = fields.Many2one('despacho.despacho', 'Despacho')
    total_qty = fields.Float('Cantidad total', digits='Product Unit of Measure', compute='_compute_total_qty')
    total_weight = fields.Float('Kg', digits='Product Unit of Measure', compute='_compute_total_qty')
    partner_city = fields.Char('Ciudad', related='partner_id.city')

    @api.depends('order_line')
    def _compute_total_qty(self):
        for record in self:
            record.total_qty = sum(record.order_line.mapped('product_uom_qty'))
            total_weight = 0
            for line in record.order_line:
                total_weight += line.product_uom_qty * line.product_id.weight
            record.total_weight = total_weight
            # record.total_weight = sum(record.order_line.mapped('product_id.weight'))
