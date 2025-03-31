from odoo import api, fields, models

import logging




class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    tag_ids = fields.Many2many(
        related='product_id.tag_ids',
        string='Tags',
    )
