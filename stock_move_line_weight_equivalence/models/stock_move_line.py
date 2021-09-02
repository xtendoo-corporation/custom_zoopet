# -- coding: utf-8 --

from odoo import api, models, fields


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    weight_amount = fields.Float(
        compute="_compute_weight_qty_done",
        readonly=True,
        store=True,
        string="Weight done",
        digits="Product Unit of Measure"
    )

    @api.onchange('qty_done')
    def _compute_weight_qty_done(self):
        self.weight_amount = 0.0
        for line in self.filtered(lambda x: x.product_id.weight > 0.0):
            line.weight_amount = line.product_id.weight * line.qty_done
