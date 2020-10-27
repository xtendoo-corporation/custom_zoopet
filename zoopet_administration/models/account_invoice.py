# -*- coding: utf-8 -*-

from odoo import api, models, fields, tools, _


class AccountInvoice(models.Model):
    _inherit = ["account.invoice", "administrator.mixin.rule"]
    _name = "account.invoice"

    delivery_method = fields.Char(
        compute="_delivery_method",
        string="Delivery Method",
        default=lambda self: self._get_delivery_method(),
    )

    @api.one
    def _delivery_method(self):

        delivery_method = self.env["sale.order"].search([("name", "=", self.origin)])
        if delivery_method:
            self.delivery_method = delivery_method[0].carrier_id.name
        else:
            self.delivery_method = ""

    @api.model
    def _get_delivery_method(self):

        delivery_method = self.env["sale.order"].search([("name", "=", self.origin)])
        if delivery_method:
            delivery_method = delivery_method[0].carrier_id.name
            return delivery_method
        else:
            return
