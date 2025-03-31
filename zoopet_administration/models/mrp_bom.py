# -- coding: utf-8 --

from odoo import api, models, fields


class MrpBom(models.Model):
    _inherit = "mrp.bom"
    _name = "mrp.bom"

    to_print = fields.Boolean(string='To Print', store=True, default=False)
