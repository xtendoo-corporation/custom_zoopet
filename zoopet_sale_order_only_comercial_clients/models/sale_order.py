# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("partner_id")
    def _get_domain(self):
        if self.env["res.users"].has_group(
                "zoopet_administration.comercial_group"
            ):
            domain = {
                "partner_id": [
                    ("user_id", "=", self.env.user.id),
                    ("parent_id", "=", False),
                ]
            }

        else:
            domain = {
                "partner_id": [("customer", "=", True), ("parent_id", "=", False)]
            }

        return {"domain": domain}

