from odoo import models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def open_produce_product(self):
        """ Se busca un lote con el mismo nombre de la orden de producción,
            de lo contrario se crea uno nuevo y se establece por defecto.
        """
        action = super().open_produce_product()
        finished_lot = self.env['stock.production.lot'].search([('name', '=', self.name)])
        if not finished_lot:
            finished_lot = self.env['stock.production.lot'].create({
                'name': self.name,
                'product_id': self.product_id.id,
                'company_id': self.company_id.id,
            })
        action['context'] = {'default_finished_lot_id': finished_lot.id}
        return action
