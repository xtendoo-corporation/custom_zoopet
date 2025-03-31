from odoo import api, models, _
from odoo.exceptions import UserError

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def render_qweb_pdf(self, res_ids=None, data=None):
        if self.name == 'Etiquetas 2.5 x 3.8 Zoopet' or self.name == 'Etiquetas 5 x 10 Zoopet':
            if not self._check_condition_zoopet(res_ids):
                return
        if self.name == 'Etiquetas 2.5 x 3.8 Petpoint' or self.name == 'Etiquetas 5 x 10 Petpoint':
            if not self._check_condition_petpoint(res_ids):
                return
        return super().render_qweb_pdf(res_ids, data)

    def _check_condition_zoopet(self, res_id):
        picking = self.env["stock.picking"].search(
            [("id", "=", res_id[0])]
        )
        for move in picking.move_ids_without_package:
            if move.price_to_print_zoopet == 0.00 and move.to_print:
                raise UserError(_("Uno o varios productos que desea imprimir no pertenecen a la tarifa Zoopet"))
        return True

    def _check_condition_petpoint(self, res_id):
        picking = self.env["stock.picking"].search(
            [("id", "=", res_id[0])]
        )
        for move in picking.move_ids_without_package:
            if move.price_to_print_petpoint == 0.00 and move.to_print:
                raise UserError(_("Uno o varios productos que desea imprimir no pertenecen a la tarifa Petpoint"))
        return True

