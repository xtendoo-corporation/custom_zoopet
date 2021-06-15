# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging

class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_ids = fields.Many2one(
        comodel_name='stock.picking', string='Delivery', invisible=True,
        default=lambda self: self._get_delivery_ids(),
        compute="_delivery_ids")

    def _delivery_ids(self):
        self.delivery_ids = self.env['stock.picking'].search(
            [('sale_id', '=', self.id)], limit=1)

    def _get_delivery_ids(self):
        delivery_ids= self.env['stock.picking'].search(
            [('sale_id', '=', self.id)], limit=1)
        return delivery_ids


