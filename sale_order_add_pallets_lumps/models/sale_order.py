# -- coding: utf-8 --

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = ["sale.order", "administrator.mixin.rule"]
    _name = "sale.order"

    lumps_number= fields.Integer(string='Lumps Number', store=True)

    pallets_number = fields.Integer(string='Palets Number', store=True)



