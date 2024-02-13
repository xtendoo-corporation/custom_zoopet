# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def select_all_lines_to_print(self):
        print("*"*80)
        print("select_all_lines_to_print", self.move_ids_without_package)
        print("*"*80)
        for line in self.move_ids_without_package:
            line.to_print = True
            line.calculate_prices_to_print()


