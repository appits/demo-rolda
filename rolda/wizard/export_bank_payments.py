import time
import base64

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class WzExportBankPayments(models.TransientModel):
    _name = 'wz.export.bank.payments'
    _description = 'Exportar pagos de bancos'

    bank_id = fields.Many2one('account.journal', 'Banco')
    date_start = fields.Date('Fecha inicio')
    date_end = fields.Date('Fecha fin')
    txt_file = fields.Binary('Archivo TXT')
    txt_name = fields.Char('Filename txt')

    def generate_banesco(self):
        payments = self.env['account.payment'].search([
            ('journal_id', '=', self.bank_id.id),
            ('payment_date', '>=', self.date_start),
            ('payment_date', '<=', self.date_end),
            ('payment_type', '=', 'outbound'),
        ])
        txt_data = ''
        for pay in payments:
            txt_data += '{:<3}|{:<15}|{:<1}|{:<6}|{:<6}|{:<1}|\n\
                {:<2}|{:<35}|{:<3}|{:<35}|{:%Y%m%d%H%M%S}|\n\
                {:<2}|{:<30}|{:<17}|{:<35}|{:0>15}|{:<3}|{:<1}|{:<34}|{:<11}|{:%Y%m%d}\n'.format(
                'HDR', 'BANESCO', 'E', 'D  95B', 'PAYMUL', 'P',
                '01', 'SCV', '9', pay.name, pay.create_date,
                '02', pay.communication, pay.company_id.vat, pay.company_id.name, pay.amount, pay.currency_id.name, '', pay.journal_id.bank_account_id.acc_number, 'BANESCO', pay.payment_date
            )
        return txt_data

    def _write_attachment(self, root):
        """ Encrypt txt, save it to the db and view it on the client as an
        attachment
        @param root: location to save document
        """
        fecha = time.strftime('%Y_%m_%d_%H%M%S')
        txt_name = f'BANESCO_{fecha}.txt'
        txt_file = root.encode('utf-8')
        txt_file = base64.encodestring(txt_file)
        self.write({'txt_name': txt_name, 'txt_file': txt_file})
        return txt_file, txt_name

    def action_export_txt(self):
        """ Exportar el documento en texto plano. """
        self.ensure_one()
        data = ''
        if 'Banesco' in self.bank_id.name:
            root = self.generate_banesco()
            data, filename = self._write_attachment(root)
        if not data:
            raise ValidationError('No se pudo generar el archivo. Intente de nuevo con otra fecha u otro banco.')
        IrConfig = self.env['ir.config_parameter'].sudo()
        base_url = IrConfig.get_param('report.url') or IrConfig.get_param('web.base.url')
        IrAttachment = self.env['ir.attachment'].sudo()
        # Guardado del archivo
        att = IrAttachment.create({
            'name': filename,
            'type': 'binary',
            'datas': data,
            'res_model': self._name,
            'res_id': self.id,
        })
        return {
            'type': 'ir.actions.act_url',
            'url': '{}/web/content/{}?download=true'.format(base_url, att.id),
            'target': self
        }
