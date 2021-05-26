from odoo import models, fields
from odoo.exceptions import UserError


class WzDespachoPrintGuide(models.TransientModel):
    """ Impresión de guías de despacho. """
    _name = 'wz.despacho.print.guide'
    _description = 'Impresión de guías de despacho'

    def _default_domain_partner(self):
        res_model = self._context.get('active_model')
        res_id = self._context.get('active_id')
        despacho = self.env[res_model].browse(res_id)
        return despacho.line_ids.mapped('partner_id.id')

    option = fields.Selection([
        ('consolidated', 'Consolidado'),
        ('by_customer', 'Por Cliente'),
        ('by_transport', 'Por Transporte'),
        ('farmatodo', 'Farmatodo'),
    ], string='Opción', default='consolidated', required=True)
    partner_id = fields.Many2one('res.partner', 'Cliente')
    domain_partner_ids = fields.Many2many('res.partner', 'partner_wz_despacho_rel', 'wz_despacho_id', 'partner_id', string='Domain de Clientes', default=_default_domain_partner)

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
        for line in despacho.line_ids:
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
            # 'date': despacho.date,
            'lines': [],
        }
        if self.partner_id:
            invoices = despacho.line_ids.filtered(lambda x: x.partner_id == self.partner_id)
        else:
            invoices = despacho.line_ids
        vals['inv_amount_total'] = sum(invoices.mapped('amount_total'))
        for line in invoices.invoice_line_ids:
            vals['lines'].append({
                'barcode': line.product_id.barcode,
                'name': line.name,
                'package': line.product_id.weight * line.quantity,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
                'discount': line.discount,
                'price_subtotal': line.price_subtotal,
            })
        datas = self._get_report_data()
        datas['despacho'] = vals
        return self.env.ref('despacho_rolda.report_guide_customer').report_action([], data=datas)

    def _report_by_transport(self, despacho):
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
        invoices = despacho.line_ids
        vals['inv_amount_total'] = sum(invoices.mapped('amount_total'))
        vals['total_weight'] = sum(invoices.mapped('total_weight'))
        for line in invoices.invoice_line_ids:
            vals['lines'].append({
                'barcode': line.product_id.barcode,
                'name': line.name,
                'package': line.product_id.weight * line.quantity,
                'quantity': line.quantity,
                # 'presentation': line.presentation,
                # 'price_subtotal': line.price_subtotal,
            })
        datas = self._get_report_data()
        datas['despacho'] = vals
        return self.env.ref('despacho_rolda.report_guide_transport').report_action([], data=datas)

    def print_report(self):
        res_model = self._context.get('active_model')
        res_id = self._context.get('active_id')
        despacho = self.env[res_model].browse(res_id)
        try:
            ref_function = getattr(self, f'_report_{self.option}')
        except AttributeError as exc:
            raise UserError(f'No existe definición de método para: _report_{self.option}()')
        return ref_function(despacho)

    def _get_display_name(self):
        ''' Helper to get the display name of an report depending of its option.
        :return:            A string representing the report.
        '''
        # Verificar funcionalidad.
        self.ensure_one()
        res_model = self._context.get('active_model')
        res_id = self._context.get('active_id')
        despacho = self.env[res_model].browse(res_id)
        report_name = 'Despacho: '
        report_name += {
            'consolidated': 'Consolidado',
            'by_customer': self.partner_id.name,
            'by_transport': despacho.transport_company_id.name,
            'farmatodo': 'Farmatodo',
        }[self.option]
        print(f'\n\n{report_name}')
        return report_name
