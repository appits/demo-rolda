from odoo import models, fields, api
from odoo.exceptions import UserError


class WzDespachoPrintGuide(models.TransientModel):
    """ Impresión de guías de despacho. """
    _name = 'wz.despacho.print.guide'
    _description = 'Impresión de guías de despacho'

    def _default_despacho(self):
        return self._context.get('active_id')

    def _default_domain_partner(self):
        res_model = self._context.get('active_model')
        res_id = self._context.get('active_id')
        despacho = self.env[res_model].browse(res_id)
        return despacho.order_ids.mapped('partner_id.id')

    option = fields.Selection([
        ('consolidated', 'Consolidado'),
        # ('by_customer', 'Por Cliente'),
        ('detailed', 'Detallado'),
        # ('farmatodo', 'Farmatodo'),
    ], string='Opción', default='consolidated', required=True)
    partner_id = fields.Many2one('res.partner', 'Cliente')
    despacho_id = fields.Many2one('despacho.despacho', 'Despacho', default=_default_despacho)
    domain_partner_ids = fields.Many2many('res.partner', 'partner_wz_despacho_rel', 'wz_despacho_id', 'partner_id', string='Domain de Clientes', default=_default_domain_partner)

    @api.onchange('option')
    def _onchange_option(self):
        if self.option == 'farmatodo':
            farmatodo_partner = self.env['res.partner'].search([
                ('name', 'ilike', 'farmatodo')], limit=1)
            self.partner_id = farmatodo_partner.id
        else:
            self.partner_id = False

    def _get_report_data(self):
        return {
            'model': self._name,
            'form': self.read()[0],
        }

    def _report_consolidated(self, despacho):
        vals = {
            'name': despacho.name,
            'transport_name': despacho.transport_company_id.name,
            'license': despacho.license_plate,
            'driver_name': despacho.driver_id.name,
            'driver_vat': despacho.vat,
            'assistant_name': despacho.assistant_id.name,
            'assistant_vat': despacho.vat_assistant,
            'notes': despacho.notes,
            'seal': despacho.seal,
            'lines': [],
        }
        for line in despacho.order_ids:
            vals['lines'].append({
                'name': line.name,
                'partner_name': line.partner_id.name,
                'partner_city': line.partner_city,
                'quantity': line.total_qty,
                'weight': line.total_weight,
            })
        datas = self._get_report_data()
        datas['despacho'] = vals
        return self.env.ref('despacho_rolda.report_guide_consolidated').report_action([], data=datas)

    def _report_by_customer(self, despacho):
        vals = {
            'name': despacho.name,
            'partner_city': self.partner_id.city,
            'partner_name': self.partner_id.name,
            'partner_vat': self.partner_id.vat,
            # 'payment_term_name': despacho.seal,
            'date': f'{despacho.date:%d/%m/%Y %H:%M}',
            'lines': [],
        }
        if self.partner_id:
            invoices = despacho.order_ids.filtered(lambda x: x.partner_id == self.partner_id)
        else:
            invoices = despacho.order_ids
        vals['inv_amount_total'] = sum(invoices.mapped('amount_total'))
        for line in invoices.order_line:
            vals['lines'].append({
                'barcode': line.product_id.barcode,
                'name': line.name,
                'package': line.product_id.weight * line.product_uom_qty,
                'quantity': line.product_uom_qty,
                'price_unit': line.price_unit,
                'discount': line.discount,
                'price_subtotal': line.price_subtotal,
            })
        datas = self._get_report_data()
        datas['despacho'] = vals
        return self.env.ref('despacho_rolda.report_guide_customer').report_action([], data=datas)

    def _report_detailed(self, despacho):
        vals = {
            'name': despacho.name,
            'transport_name': despacho.transport_company_id.name,
            'license': despacho.license_plate,
            'driver_name': despacho.driver_id.name,
            'driver_vat': despacho.vat,
            'assistant_name': despacho.assistant_id.name,
            'assistant_vat': despacho.vat_assistant,
            'notes': despacho.notes,
            'seal': despacho.seal,
            'lines': [],
        }
        invoices = despacho.order_ids
        vals['inv_amount_total'] = sum(invoices.mapped('amount_total'))
        vals['total_weight'] = sum(invoices.mapped('total_weight'))
        for line in invoices.order_line:
            vals['lines'].append({
                'barcode': line.product_id.barcode,
                'name': line.name,
                'package': line.product_id.weight * line.product_uom_qty,
                'quantity': line.product_uom_qty,
                'uom_name': line.product_uom.name,
                # 'price_subtotal': line.price_subtotal,
            })
        datas = self._get_report_data()
        datas['despacho'] = vals
        return self.env.ref('despacho_rolda.report_guide_detailed').report_action([], data=datas)

    def _report_farmatodo(self, despacho):
        vals = {
            'name': despacho.name,
            'transport_name': despacho.transport_company_id.name,
            'license': despacho.license_plate,
            'driver_name': despacho.driver_id.name,
            'driver_vat': despacho.vat,
            'assistant_name': despacho.assistant_id.name,
            'assistant_vat': despacho.vat_assistant,
            'notes': despacho.notes,
            'seal': despacho.seal,
            'lines': [],
        }
        if self.partner_id:
            invoices = despacho.order_ids.filtered(lambda x: x.partner_id == self.partner_id)
        else:
            raise UserError('Debes seleccionar un Cliente con nombre Farmatodo.')
        vals['inv_amount_total'] = sum(invoices.mapped('amount_total'))
        for line in invoices:
            vals['lines'].append({
                'name': line.name,
                'partner_name': line.partner_id.name,
                'partner_city': line.partner_id.city,
                'quantity': line.total_qty,
                'weight': line.total_weight,
            })
        datas = self._get_report_data()
        datas['despacho'] = vals
        return self.env.ref('despacho_rolda.report_guide_farmatodo').report_action([], data=datas)

    def print_report(self):
        res_model = self._context.get('active_model')
        res_id = self._context.get('active_id')
        despacho = self.env[res_model].browse(res_id)
        try:
            ref_function = getattr(self, f'_report_{self.option}')
        except AttributeError as exc:
            raise UserError(f'No existe definición de método para: _report_{self.option}()')
        return ref_function(despacho)
