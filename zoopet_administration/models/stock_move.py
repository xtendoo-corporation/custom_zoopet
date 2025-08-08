# -*- coding: utf-8 -*-

from odoo import api, models, fields, tools, _
from odoo.tools import float_compare, float_round, float_is_zero


class AccountMove(models.Model):
    _inherit = ["stock.move"]
    _name = "stock.move"

    def _compute_kit_quantities(self, product_id, kit_qty, kit_bom, filters):
        """ Computes the quantity delivered or received when a kit is sold or purchased.
        A ratio 'qty_processed/qty_needed' is computed for each component, and the lowest one is kept
        to define the kit's quantity delivered or received.
        :param product_id: The kit itself a.k.a. the finished product
        :param kit_qty: The quantity from the order line
        :param kit_bom: The kit's BoM
        :param filters: Dict of lambda expression to define the moves to consider and the ones to ignore
        :return: The quantity delivered or received
        """
        qty_ratios = []
        boms, bom_sub_lines = kit_bom.explode(product_id, kit_qty)
        for bom_line, bom_line_data in bom_sub_lines:
            bom_line_moves = self.filtered(lambda m: m.bom_line_id == bom_line)
            if bom_line_moves:
                if float_is_zero(bom_line_data['qty'], precision_rounding=bom_line.product_uom_id.rounding):
                    # As BoMs allow components with 0 qty, a.k.a. optionnal components, we simply skip those
                    # to avoid a division by zero.
                    continue
                # We compute the quantities needed of each components to make one kit.
                # Then, we collect every relevant moves related to a specific component
                # to know how many are considered delivered.
                uom_qty_per_kit = bom_line_data['qty'] / bom_line_data['original_qty']
                qty_per_kit = bom_line.product_uom_id._compute_quantity(uom_qty_per_kit, bom_line.product_id.uom_id, round=False)
                if not qty_per_kit:
                    continue
                incoming_moves = bom_line_moves.filtered(filters['incoming_moves'])
                outgoing_moves = bom_line_moves.filtered(filters['outgoing_moves'])
                qty_processed = sum(incoming_moves.mapped('product_qty')) - sum(outgoing_moves.mapped('product_qty'))
                # We compute a ratio to know how many kits we can produce with this quantity of that specific component
                qty_ratios.append(qty_processed / qty_per_kit)
            else:
                return 0.0
        if qty_ratios:
            # Now that we have every ratio by components, we keep the lowest one to know how many kits we can produce
            # with the quantities delivered of each component. We use the floor division here because a 'partial kit'
            # doesn't make sense.
            print("*"*120)
            print("entra", min(qty_ratios))
            print("*"*120)
            return min(qty_ratios)
        else:
            return 0.0

class StockMove(models.Model):
    _inherit = 'stock.move.line'

    def _compute_sale_order_line_fields(self):
        """This is computed with sudo for avoiding problems if you don't have
        access to sales orders (stricter warehouse users, inter-company
        records...).
        """
        self.sale_tax_description = False
        self.sale_price_subtotal = False
        self.sale_price_tax = False
        self.sale_price_total = False
        self.sale_price_unit = False
        for line in self:
            valued_line = line.sale_line
            if not valued_line:
                continue
            quantity = line._get_report_valued_quantity()
            sale_line_uom = valued_line.product_uom
            different_uom = valued_line.product_uom != line.product_uom_id
            different_qty = float_compare(
                quantity,
                line.sale_line.product_uom_qty,
                precision_rounding=line.product_uom_id.rounding,
            )
            # --- INICIO CAMBIO KIT ---
            # Si el producto de la línea de venta es un kit, usar el precio del kit y no el de los componentes
            bom_kit = self.env['mrp.bom'].search([
                ('product_tmpl_id', '=', valued_line.product_id.product_tmpl_id.id),
                ('type', '=', 'phantom')
            ], limit=1)
            if bom_kit:
                # El producto es un kit, usar el precio unitario y total de la línea de venta original
                price_unit = line.sale_line.price_unit
                # Calcula impuestos igual que el cálculo original
                taxes = line.sale_line.tax_id.compute_all(
                    price_unit,
                    line.sale_line.order_id.currency_id,
                    quantity,
                    product=line.sale_line.product_id,
                    partner=line.sale_line.order_id.partner_shipping_id,
                )
                price_subtotal = taxes['total_excluded']
                price_tax = taxes['total_included'] - taxes['total_excluded']
                price_total = taxes['total_included']
                line.update({
                    "sale_tax_description": ", ".join(
                        t.name or t.description for t in line.sale_tax_id
                    ),
                    "sale_price_subtotal": price_subtotal,
                    "sale_price_tax": price_tax,
                    "sale_price_total": price_total,
                    "sale_price_unit": price_unit,
                })
            else:
                if different_uom or different_qty:
                    # Force read to cache M2M field for get values with _convert_to_write
                    line.sale_line.mapped("tax_id")
                    # Create virtual sale line with stock move line quantity
                    sol_vals = line.sale_line._convert_to_write(line.sale_line._cache)
                    valued_line = line.sale_line.new(sol_vals)
                    valued_line.product_uom_qty = quantity
                if different_qty:
                    # Force original price unit to avoid pricelist recomputed (not needed)
                    valued_line.price_unit = line.sale_line.price_unit
                if different_uom:
                    valued_line.price_unit = sale_line_uom._compute_price(
                        valued_line.price_unit, line.product_uom_id
                    )
            line.update(
                {
                    "sale_tax_description": ", ".join(
                        t.name or t.description for t in line.sale_tax_id
                    ),
                    "sale_price_subtotal": valued_line.price_subtotal,
                    "sale_price_tax": valued_line.price_tax,
                    "sale_price_total": valued_line.price_total,
                    "sale_price_unit": valued_line.price_unit,
                }
            )
