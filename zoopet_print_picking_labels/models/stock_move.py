# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = "stock.move"

    to_print = fields.Boolean(
        string="Imprimir",
        default=False
    )
    price_to_print_zoopet = fields.Float("Price to print zoopet", digits="Product Price", default=0.0 )
    price_to_print_petpoint = fields.Float("Price to print petpoint", digits="Product Price", default=0.0)

    @api.onchange('to_print')
    def calculate_prices_to_print(self):
        self.price_to_print_zoopet = self.get_price_with_tax(self.calculate_pricelist_price('Zoopet'))
        self.price_to_print_petpoint = self.get_price_with_tax(self.calculate_pricelist_price('Petpoint'))

    def calculate_pricelist_price(self, pricelistName):
        price = 0.00
        pricelist = self.env["product.pricelist"].search(
            [("name", "=", pricelistName)]
        )
        if pricelist:
            pricelist_item = self.env["product.pricelist.item"].search(
                [("pricelist_id", "=", pricelist.id)]
            )
            for item in pricelist_item:
                if item.applied_on == '1_product' and item.product_tmpl_id.id == self.product_id.id:
                    return pricelist.price_get(self.product_id.id, 1)[pricelist.id]
                if item.applied_on == '0_product_variant' and item.product_id.id == self.product_id.id:
                    return pricelist.price_get(self.product_id.id, 1)[pricelist.id]
                if item.applied_on == '3_global':
                    price = pricelist.price_get(self.product_id.id, 1)[pricelist.id]
        return price

    def get_price_with_tax(self, price):
        taxes = self.product_id.taxes_id.compute_all(price, self.product_id.currency_id, 1, self.product_id)
        return taxes['total_included']

