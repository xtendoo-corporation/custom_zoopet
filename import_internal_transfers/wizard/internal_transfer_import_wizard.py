import logging
import base64

import xlrd

from odoo import _, fields, api, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

try:
    from csv import reader
except (ImportError, IOError) as err:
    _logger.error(err)


class InternalTransferImport(models.TransientModel):
    _name = "internal.transfer.import"
    _description = "Internal Transfer Import"

    import_file = fields.Binary(string="Import File (*.xlsx)")

    picking_type_id = fields.Many2one(
        comodel_name="stock.picking.type",
        string="Allowed operation type",
        domain="[('code', '=', 'internal')]",
        required=True,
    )
    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        auto_join=True, index=True, required=True,
        help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations.")
    location_dest_id = fields.Many2one(
        'stock.location', 'Destination Location',
        auto_join=True, index=True, required=True,
        help="Location where the system will stock the finished products.")

    @api.onchange("picking_type_id")
    def _compute_location(self):
        for record in self:
            record.location_id = record.picking_type_id.default_location_src_id
            record.location_dest_id = record.picking_type_id.default_location_dest_id

    def action_import_file(self):
        """ Process the file chosen in the wizard, create bank statement(s) and go to reconciliation. """
        self.ensure_one()
        if self.import_file:
            self._import_record_data(self.import_file)
        else:
            raise ValidationError(_("Please select Excel file to import"))

    @api.model
    def _import_record_data(self, import_file):
        try:
            decoded_data = base64.decodebytes(import_file)
            workbook = xlrd.open_workbook(file_contents=decoded_data)
            sheet = workbook.sheet_by_index(0)
            lines_to_add = self._prepare_internal_transfer_lines(sheet)
            if not lines_to_add:
                raise ValidationError(
                    _('No hay lineas válidas que añadir.')
                )
            self.create_internal_transfer(lines_to_add)
        except xlrd.XLRDError:
            raise ValidationError(
                _("Formato no válido")
            )

    def _prepare_internal_transfer_lines(self, sheet):
        lines = []
        for row_index in range(sheet.nrows):
            if row_index > 0:
                if sheet.cell_value(row_index, 0):
                    product = sheet.cell_value(row_index, 0)
                    partes = product.split("]")
                    codigo = partes[0][1:]
                    descripcion = partes[1].strip()
                    product_id = self.env["product.product"].search(
                        [("default_code", "=", codigo), ("name", "=", descripcion)])
                    if product_id:
                        lines.append(
                            {
                                "product_id": product_id.id,
                                "description_picking": descripcion,
                                "quantity_done": sheet.cell_value(row_index, 1),
                                "product_uom": product_id.uom_id.id,
                            })

        return lines

    def create_internal_transfer(self, lines):
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.picking_type_id.id,
                "location_id": self.location_id.id,
                "location_dest_id": self.location_dest_id.id,
                "move_ids_without_package": [
                    (0, 0, {"product_id": line["product_id"], "name": line["description_picking"],"quantity_done": line["quantity_done"], "product_uom": line["product_uom"], "location_id": self.location_id.id, "location_dest_id": self.location_dest_id.id})
                    for line in lines
                ],
            }
        )
        picking.action_confirm()
        # picking.action_assign()
        # picking.button_validate()
        return picking
