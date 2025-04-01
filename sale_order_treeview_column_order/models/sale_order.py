from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    total_ordered_weight_display = fields.Float(
        string="Total Peso Pedido",
        compute="_compute_total_ordered_weight_display",
        store=False
    )

    total_delivered_weight_display = fields.Float(
        string="Total Peso Enviado",
        compute="_compute_total_delivered_weight_display",
        store=False
    )

    def _compute_total_ordered_weight_display(self):
        for order in self:
            order.total_ordered_weight_display = order.total_weight()

    def _compute_total_delivered_weight_display(self):
        for order in self:
            order.total_delivered_weight_display = sum(
                line.qty_delivered * line.product_id.weight
                for line in order.order_line if line.product_id and line.product_id.weight
            )
