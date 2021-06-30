# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class StockMove(models.Model):
    _inherit = 'stock.move'

    cal_units = fields.Integer(string="Units",compute='_compute_units')


    def _compute_units(self):
        for line in self:
            presentation=line.product_id.product_tmpl_id.presentation            
            if presentation > 0:
                cal=presentation*line.product_uom_qty
                line.cal_units=cal
            else:
                line.cal_units=0

