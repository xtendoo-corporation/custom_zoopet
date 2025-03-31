# -*- coding: utf-8 -*-

from odoo import api, models, fields, tools, _


class AccountMove(models.Model):
    _inherit = ["account.move", "administrator.mixin.rule"]
    _name = "account.move"

    delivery_method = fields.Char(
        compute="_delivery_method",
        string="Delivery Method",
        default=lambda self: self._get_delivery_method(),
    )

    def _delivery_method(self):
        for invoice in self:
            sale_order = self.env["sale.order"].search([("name", "=", invoice.invoice_origin)])
            if sale_order:
                invoice.delivery_method = sale_order[0].carrier_id.name
            else:
                invoice.delivery_method = ""

    def _get_delivery_method(self):
        sale_order = self.env["sale.order"].search([("name", "=", self.invoice_origin)])
        if sale_order:
            return sale_order[0].carrier_id.name
        else:
            return ''
