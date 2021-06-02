# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderTypology(models.Model):
    _inherit = 'sale.order.type'

    fiscal_position_id = fields.Many2one(
        comodel_name='account.fiscal.position', string='Fiscal Position',
        )