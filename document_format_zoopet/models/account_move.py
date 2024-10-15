# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools import float_is_zero
from collections import OrderedDict


class AccountMove(models.Model):
    _inherit = "account.move"

    refund_invoice_name = fields.Char(
        compute='_refund_invoice_name',
        )

    def _refund_invoice_name(self):
        if self.type == 'out_refund':
            if not self.refund_invoice_id:
                if self.invoice_origin:
                    invoice=self.env['account.move'].search_read([('invoice_origin', '=', self.invoice_origin), ('type', '=', 'out_invoice')],['id', 'number'], limit=1)
                    if invoice:
                        self.refund_invoice_name= invoice[0]['number']
            else:
                self.refund_invoice_name = self.refund_invoice_id.number
        else:
            self.refund_invoice_name= ""

    def _sort_grouped_lines(self, lines_dic):
        return sorted(lines_dic, key=lambda x: (
            x['picking'].date, x['picking'].date_done))

    def _get_signed_quantity_done(self, invoice_line, move, sign):
        """Hook method. Usage example:
        account_invoice_report_grouped_by_picking_sale_mrp module
        """
        qty = 0
        if move.location_id.usage == 'customer':
            qty = -move.quantity_done * sign
        elif move.location_dest_id.usage == 'customer':
            qty = move.quantity_done * sign
        return qty

    def lines_grouped_by_picking(self):
        """This prepares a data structure for printing the invoice report
        grouped by pickings."""
        self.ensure_one()
        picking_dict = OrderedDict()
        lines_dict = OrderedDict()
        sign = -1.0 if self.type == 'out_refund' else 1.0
        # Let's get first a correspondance between pickings and sales order
        pickings = self.mapped('invoice_line_ids.move_line_ids.picking_id')
        so_dict = {x.sale_id: x for x in pickings if x.sale_id}
        # Now group by picking by direct link or via same SO as picking's one
        for line in self.invoice_line_ids:
            remaining_qty = line.quantity
            for move in line.move_line_ids:
                key = (move.picking_id, line)
                picking_dict.setdefault(key, 0)
                qty = self._get_signed_quantity_done(line, move, sign)
                picking_dict[key] += qty
                remaining_qty -= qty
            if not line.move_line_ids and line.sale_line_ids:
                for so_line in line.sale_line_ids:
                    if so_dict.get(so_line.order_id):
                        key = (so_dict[so_line.order_id], line)
                        picking_dict.setdefault(key, 0)
                        qty = so_line.product_uom_qty
                        picking_dict[key] += qty
                        remaining_qty -= qty
            if (not float_is_zero(
                    remaining_qty,
                    precision_rounding=0.01)):
                lines_dict[line] = remaining_qty
        no_picking = [
            {'picking': False, 'line': key, 'quantity': value}
            for key, value in lines_dict.items()
        ]
        with_picking = [
            {'picking': key[0], 'line': key[1], 'quantity': value}
            for key, value in picking_dict.items()
        ]
        return self._sort_grouped_lines(with_picking)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_sorted_taxes(self):
        return self.tax_ids.sorted(lambda tax: tax.tax_group_id.sequence)

