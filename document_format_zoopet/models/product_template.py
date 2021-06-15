# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    bom_ids = fields.Many2one(
        comodel_name='mrp.bom', string='Lista de materiales', invisible=True,
        default=lambda self: self._get_bom_ids(),
        compute="_bom_ids")

    def _bom_ids(self):
        self.bom_ids = self.env['mrp.bom'].search(
            [('product_tmpl_id', '=', self.id)], limit=1)

    def _get_bom_ids(self):
        bom_ids= self.env['mrp.bom'].search(
            [('product_tmpl_id', '=', self.id)], limit=1)
        return bom_ids
