from odoo import models, api


class IvaReport(models.AbstractModel):
    _inherit = 'report.locv_withholding_iva.template_wh_vat'

    @api.model
    def _get_report_values(self, docids, data=None):
        values = super()._get_report_values(docids, data)
        tax_base = {}
        tax_general = {}
        taxes = []
        for b_amount in values['base_amount']:
            tax_base.setdefault(b_amount['rate_general'], []).append(self.decode_separador_cifra(b_amount['base_general']))
            tax_general.setdefault(b_amount['rate_general'], []).append(self.decode_separador_cifra(b_amount['tax_general']))
            taxes.append(b_amount['rate_general'])
        # Suma los valores de la lista de cada clave
        for key, vals in tax_base.items():
            tax_base[key] = self.separador_cifra(sum(vals))
        for key, vals in tax_general.items():
            tax_general[key] = self.separador_cifra(sum(vals))
        values.update({
            'amount_tax_base': tax_base,
            'amount_tax_general': tax_general,
            'taxes_name': set(taxes),
        })
        return values

    def decode_separador_cifra(self, valor):
        """ Convierte el param: valor str() en float() """
        monto = valor.replace(',', '-').replace('.', '').replace('-', '.')
        return float(monto)
