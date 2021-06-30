# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class ProductTemplate(models.Model):
    _inherit = 'product.template'

    presentation = fields.Integer('Presentation')


