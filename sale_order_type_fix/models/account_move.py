# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging


class AccountMove(models.Model):
    _inherit = "account.move"

    sale_type_id = fields.Many2one(
        comodel_name="sale.order.type",
        string="Sale Type",
        compute="",
        store=True,
        readonly=False,
        states={"posted": [("readonly", True)], "cancel": [("readonly", True)]},
        copy=True,
    )

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        res.update({"sale_type_id": self._compute_sale_type_id(vals)})
        return res

    def _compute_sale_type_id(self, vals):
        sale_type_id = False

        if vals.get('type') in ["out_invoice", "out_refund"] and vals.get('invoice_origin'):
            # Intentamos encontrar la factura original para heredar el tipo de venta
            refunded_invoice = self.env["account.move"].search(
                [
                    ("invoice_origin", "=", vals.get("invoice_origin")),
                    ("type", "=", "out_invoice"),
                    ("state", "=", "posted"),
                ],
                limit=1
            )
            if refunded_invoice:
                sale_type_id = refunded_invoice.sale_type_id

        # Si no lo conseguimos por origen, tomamos el valor directo si lo trae
        if not sale_type_id and vals.get('sale_type_id'):
            sale_type_id = self.env['sale.order.type'].browse(vals['sale_type_id'])

        # Si aún no se tiene, buscamos por origen del pedido
        if not sale_type_id and vals.get('invoice_origin'):
            sale_order = self.env['sale.order'].search([('name', '=', vals['invoice_origin'])], limit=1)
            if sale_order:
                sale_type_id = sale_order.type_id

        # Si no hay partner, usamos uno por defecto de la compañía
        if not sale_type_id and not vals.get('partner_id'):
            sale_type_id = self.env["sale.order.type"].search(
                [("company_id", "in", [self.env.company.id, False])], limit=1
            )

        # Si hay partner, intentamos sacarlo desde ahí
        elif not sale_type_id and vals.get('partner_id'):
            partner_id = self.env['res.partner'].browse(vals['partner_id'])
            sale_type = (
                partner_id.with_context(force_company=self.company_id.id).sale_type or
                partner_id.commercial_partner_id.with_context(force_company=self.company_id.id).sale_type
            )
            if sale_type:
                sale_type_id = sale_type

        return sale_type_id.id if sale_type_id else False
