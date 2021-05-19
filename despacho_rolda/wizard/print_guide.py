from odoo import models, fields


class WzDespachoPrintGuide(models.TransientModel):
    """ Impresión de guías de despacho. """
    _name = 'wz.despacho.print.guide'
    _description = 'Impresión de guías de despacho'

    option = fields.Selection([
        ('consolidated', 'Consolidado'),
        ('by_customer', 'Por Cliente'),
        ('by_transport', 'Por Transporte'),
        ('farmatodo', 'Farmatodo'),
    ], string='Opción', default='consolidated', required=True)

    def print_report(self):
        res_model = self._context.get('active_model')
        res_id = self._context.get('active_id')
        despacho = self.env[res_model].browse(res_id)
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
        datas = {
            'despacho': vals,
            'model': self._name,
            'form': self.read()[0],
        }
        if self.option == 'consolidated':
            return self.env.ref('despacho_rolda.report_guide_consolidated').report_action([], data=datas)
