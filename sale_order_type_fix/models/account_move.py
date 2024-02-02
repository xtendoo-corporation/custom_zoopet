# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging


class AccountMove(models.Model):
    _inherit = "account.move"

    sale_type_id = fields.Many2one(
        comodel_name="sale.order.type",
        string="Sale Type",
        default=lambda self: self._compute_sale_type_id(),
        compute="",
        store=True,
        readonly=False,
        states={"posted": [("readonly", True)], "cancel": [("readonly", True)]},
        copy=True,
    )

    @api.model
    def create(self, vals):
        if vals.get('sale_type_id'):
            vals['sale_type_id'] = self._compute_sale_type_id(vals)
        res = super(AccountMove, self).create(vals)
        return res

    def _compute_sale_type_id(self, vals):
        if vals.get('type') not in ["out_invoice", "out_refund"]:
            sale_type_id = self.env["sale.order.type"]
        else:
            if vals.get('invoice_origin'):
                sale_type_id = self.env['sale.order'].search([('name', '=', vals['invoice_origin'])], limit=1).type_id
            else:
                sale_type_id = vals.get('sale_type_id')
        if not vals.get('partner_id'):
            sale_type_id = self.env["sale.order.type"].search(
                [("company_id", "in", [self.env.company.id, False])], limit=1
            )
        if vals['type'] in ["out_invoice"]:
            #rectificativa desde el boton create invoice en pedidos
            refunded_invoice = self.env["account.move"].search(
                [
                    ("invoice_origin", "=", vals['invoice_origin']),
                    ("type", "=", "out_invoice"),
                    ("state", "=", "posted"),
                ], limit=1
            )
            if refunded_invoice:
                sale_type_id = refunded_invoice.sale_type_id
        if vals['type'] in ["out_refund"]:
            #rectificativa desde crear rectificativa dentro de una factura
            refunded_invoice = self.env["account.move"].search(
                [
                    ("invoice_origin", "=", vals['invoice_origin']),
                    ("type", "=", "out_invoice"),
                    ("state", "=", "posted"),
                ], limit=1
            )
            if refunded_invoice:
                sale_type_id = refunded_invoice.sale_type_id
        else:
            #Si no es ninguna, mete el del partner_id.
            partner_id = self.env['res.partner'].browse(vals['partner_id'])
            sale_type = (
                partner_id.with_context(
                    force_company=self.company_id.id
                ).sale_type
                or partner_id.commercial_partner_id.with_context(
                force_company=self.company_id.id
                ).sale_type
            )
            if sale_type:
                sale_type_id = sale_type
        return sale_type_id.id


