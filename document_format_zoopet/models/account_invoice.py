# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    refund_invoice_name = fields.Char(
        compute='_refund_invoice_name',
        )

    @api.one
    def _refund_invoice_name(self):
        if self.type == 'out_refund':
            if not self.refund_invoice_id:
                if self.origin:
                    invoice=self.env['account.invoice'].search_read([('origin', '=', self.origin), ('type', '=', 'out_invoice')],['id', 'number'], limit=1)
                    if invoice:
                        self.refund_invoice_name= invoice[0]['number']
        else:
            self.refund_invoice_name= ""
    