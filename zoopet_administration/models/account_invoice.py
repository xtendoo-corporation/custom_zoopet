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
        sale_order = self.env["sale.order"].search([("name", "=", self.origin)])
        if sale_order:
            self.delivery_method = sale_order[0].carrier_id.name
        else:
            self.delivery_method = ""

    @api.model
    def _get_delivery_method(self):
        sale_order = self.env["sale.order"].search([("name", "=", self.origin)])
        if sale_order:
            return sale_order[0].carrier_id.name
        else:
            return ''

    # @api.onchange('partner_id', 'company_id')
    # def _onchange_partner_id(self):
    #     res = super()._onchange_partner_id()
    #     if self.type in ['out_invoice', 'out_refund']:
    #         sale_order = self.env["sale.order"].search([("name", "=", self.origin)])
    #         if sale_order:
    #             print("sale order global discounts",sale_order.global_discount_ids)
    #             print("before:::::::::::::::::::::",self.global_discount_ids)
    #             self.global_discount_ids = [(6,0,[sale_order.global_discount_ids.ids])]
    #             # self.global_discount_ids = [(6, 0, [])]
    #             print("after::::::::::::::::::::::",self.global_discount_ids)
    #     return res
