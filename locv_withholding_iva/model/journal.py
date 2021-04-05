# coding: utf-8
###########################################################################


from odoo import models, fields, api, exceptions, _

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    is_withholdable = fields.Boolean(string="Ret. IVA", default=False)