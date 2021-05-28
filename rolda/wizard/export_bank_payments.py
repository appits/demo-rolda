import time
import base64

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ExportBankPayments(models.Model):
    _name = 'export.bank.payments'
    _description = 'Exportar pagos de bancos'

    _READONLY_STATES = {'done': [('readonly', True)]}

    name = fields.Char('Nombre', default='Nuevo', readonly=True)
    type_rec = fields.Char('Tipo de registro', default='01', readonly=True)
    type_trans = fields.Selection([
        ('SAL', 'Nómina'),
        ('SCV', 'Pago a proveedores')
    ], string='Tipo de transacción', readonly=True, default='SCV')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('done', 'Confirmado')
    ], string='Tipo de transacción', default='draft', copy=False)
    condition = fields.Char('Condición', default='9', readonly=True)
    bank_id = fields.Many2one('account.journal', 'Banco', states=_READONLY_STATES)
    date_start = fields.Date('Fecha inicio', states=_READONLY_STATES)
    date_end = fields.Date('Fecha fin', states=_READONLY_STATES)
    txt_file = fields.Binary('Archivo TXT', copy=False)
    txt_name = fields.Char('Filename txt', copy=False)

    @api.model
    def create(self, vals):
        new_id = super().create(vals)
        new_id.name = self.env['ir.sequence'].next_by_code('export.bank.payments')
        return new_id

    def action_draft(self):
        self.write({
            'state': 'draft',
            'txt_file': False,
            'txt_name': False,
        })
        return True

    def action_done(self):
        """ Exportar el documento en texto plano. """
        self.ensure_one()
        data = ''
        if 'Banesco' in self.bank_id.name:
            root = self.generate_banesco()
            data, filename = self._write_attachment(root, 'BANESCOPATENTE')
        if 'Exterior' in self.bank_id.name:
            root = self.generate_exterior()
            data, filename = self._write_attachment(root, 'EXTERIOR')
        if not data:
            raise ValidationError('No se pudo generar el archivo. Intente de nuevo con otra fecha u otro banco.')
        # IrAttachment = self.env['ir.attachment'].sudo()
        # # Guardado del archivo
        # att = IrAttachment.create({
        #     'name': filename,
        #     'type': 'binary',
        #     'datas': data,
        #     'res_model': self._name,
        #     'res_id': self.id,
        # })
        self.write({'state': 'done'})
        return True

    def _write_attachment(self, root, prefix):
        """ Encrypt txt, save it to the db and view it on the client as an
        attachment
        @param root: location to save document
        """
        fecha = time.strftime('%d%m%y')
        txt_name = f'{prefix}{fecha}.txt'
        txt_file = root.encode('utf-8')
        txt_file = base64.encodestring(txt_file)
        self.write({'txt_name': txt_name, 'txt_file': txt_file})
        return txt_file, txt_name

    def _get_out_payments(self):
        payments = self.env['account.payment'].search([
            ('journal_id', '=', self.bank_id.id),
            ('payment_date', '>=', self.date_start),
            ('payment_date', '<=', self.date_end),
            ('payment_type', '=', 'outbound'),
        ])
        return payments

    def generate_banesco(self):
        out_payments = self._get_out_payments()
        txt_data = ''
        if out_payments:
            # 1ra línea: Para registro de control    (inicia con: HDR)
            txt_data += f"{'HDR':<3}{'BANESCO':<15}{'E':<1}{'D  95B':<6}{'PAYMUL':<6}{'P':<1}\n"
            # 2da línea: Para registro de encabezado (inicia con: 01)
            txt_data += f'{self.type_rec:<2}{self.type_trans:<35}{self.condition:<3}{self.name:<35}{self.create_date:%Y%m%d%H%M%S}\n'
            for pay in out_payments:
                # 3ra línea: Para registro de débito (inicia con: 02)
                txt_data += '{:<2}{:<30}{:<17}{:<35}{:0>15}{:<3}{:<1}{:<34}{:<11}{:%Y%m%d}\n'.format(
                    '02', pay.communication, pay.company_id.vat, pay.company_id.name, f'{pay.amount:.2f}'.replace('.', ''), pay.currency_id.name, '', pay.journal_id.bank_account_id.acc_number, 'BANESCO', pay.payment_date
                )
            # Última línea: Para registro de totales (inicia con: 06)
            txt_data += f'{"06":<2}{len(out_payments):0>15}{"":0>15}{"":0>15}\n'
        return txt_data

    def generate_exterior(self):
        out_payments = self._get_out_payments()
        txt_data = ''
        qty_payments = len(out_payments)
        total_amount = sum(out_payments.mapped('amount'))
        # if out_payments:
        #     for partner in out_payments.mapped('partner_id'):
        #         # 1ra línea: Estructura del encabezado
        #         ident = partner.nationality if partner.company_type == 'person' else partner.vat.split('-')[0]
        #         num_ident = partner.identification_id if partner.company_type == 'person' else partner.vat and partner.vat.split('-', 1)[1]
        #         acc_number = self.bank_id.bank_account_id.acc_number
        #         txt_data += f"{ident:<1}{num_ident:0>9}{acc_number:<20}{qty_payments:0>4}{total_amount:0>13}{self.date_start:%d%m%Y}{'01':0>2}{'':<19}\n"
        #         for pay in out_payments.filtered(lambda x: x.partner_id == partner):
        #             # 2da línea: Estructura del detalle
        #             txt_data += '{:<50}{:0>12}{:<120}{:<3}{:<20}{:<50}{:0>8}{:0>11}\n'.format(
        #                 pay.partner_id.name, pay.amount, pay.name, '', '', pay.partner_id.email, pay.communication, f'{pay.partner_id.nationality}{pay.partner_id.identification_id}')
        return txt_data
