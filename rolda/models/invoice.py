from odoo import api, models, fields


class account_invoice(models.Model):
    _inherit = 'account.move'

    @api.depends('amount_total', 'currency_id')
    def _compute_amount_currency(self):
        for inv in self:

            if inv.company_currency_id and inv.company_currency_id != inv.currency_id:
                inv.amount_total_currency = inv.amount_total * inv.company_currency_id.rate
                inv.amount_untaxed_currency = inv.amount_untaxed * inv.company_currency_id.rate
                inv.amount_by_group_currency = inv.amount_total_currency - inv.amount_untaxed_currency
            else:
                inv.amount_total_currency = inv.amount_total
                inv.amount_by_group_currency = inv.amount_total - inv.amount_untaxed
                inv.amount_untaxed_currency = inv.amount_untaxed

    @api.depends('invoice_date', 'currency_id')
    def get_report_rate(self):
        for inv in self:
            rates = self.company_currency_id.rate_ids
            rate = float(0)
            
            for r in rates:
                if r.name == inv.invoice_date:
                    rate= float(r.rate)
        return rate
              

    amount_total_currency = fields.Monetary(string='Total currency', compute='_compute_amount_currency')
    amount_by_group_currency = fields.Monetary(string='Total tax currency', compute='_compute_amount_currency')
    amount_untaxed_currency = fields.Monetary(string='Total untaxed', compute='_compute_amount_currency')
