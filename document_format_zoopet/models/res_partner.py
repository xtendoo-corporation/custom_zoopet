# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    copy_num = fields.Integer(
        string='Copy number',
        default=1,
        store=True)
