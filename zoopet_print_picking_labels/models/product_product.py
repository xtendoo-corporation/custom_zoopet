# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ProductProduct(models.Model):
    _inherit = "product.product"

    price_to_print_zoopet = fields.Float("Price to print zoopet", digits="Product Price", compute="calculate_pricelist_price_zoopet")
    price_to_print_petpoint = fields.Float("Price to print petpoint", digits="Product Price", compute="calculate_pricelist_price_petpoint")

    def calculate_pricelist_price_zoopet(self):
        pricelist = self.env["product.pricelist"].search(
            [("name", "=", 'Zoopet')]
        )
        for record in self:
            price = 0.00
            if pricelist:
                pricelist_item = self.env["product.pricelist.item"].search(
                    [("pricelist_id", "=", pricelist.id)]
                )
                for item in pricelist_item:
                    if item.applied_on == '1_product' and item.product_tmpl_id.id == record.id:
                        if item.compute_price == 'fixed':
                            price = item.fixed_price
                    elif item.applied_on == '0_product_variant' and item.product_id.id == record.id:
                        if item.compute_price == 'fixed':
                            price = item.fixed_price
                    elif item.applied_on == '3_global':
                        if item.compute_price == 'fixed':
                            price = item.fixed_price
            price = record.get_price_with_tax(price)
            record.price_to_print_zoopet = price

    def calculate_pricelist_price_petpoint(self):
        pricelist = self.env["product.pricelist"].search(
            [("name", "=", 'Petpoint')]
        )
        for record in self:
            price = 0.00
            if pricelist:
                pricelist_item = self.env["product.pricelist.item"].search(
                    [("pricelist_id", "=", pricelist.id)]
                )
                for item in pricelist_item:
                    if item.applied_on == '1_product' and item.product_tmpl_id.id == record.id:
                        if item.compute_price == 'fixed':
                            price = item.fixed_price
                    elif item.applied_on == '0_product_variant' and item.product_id.id == record.id:
                        if item.compute_price == 'fixed':
                            price = item.fixed_price
                    elif item.applied_on == '3_global':
                        if item.compute_price == 'fixed':
                            price = item.fixed_price
            price = record.get_price_with_tax(price)
            record.price_to_print_petpoint = price

    def get_price_with_tax(self, price):
        taxes = self.taxes_id.compute_all(price, self.currency_id, 1, self.id)
        return taxes['total_included']
