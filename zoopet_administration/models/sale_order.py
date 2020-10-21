# -- coding: utf-8 --

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = ["sale.order", "administrator.mixin.rule"]
    _name = "sale.order"

    # Método que devuelve el warning si el cliente tiene algun tipo de notas
    @api.onchange("partner_id")
    def onchange_partner_id_warning(self):
        if not self.partner_id:
            return
        warning = {}
        title = False
        message = False
        partner_id = self.partner_id
        # Buscamos el comentario en su partner_id, y si no tiene la buscamos en su parent_id si lo tuviese
        if partner_id.comment == "" and partner_id.parent_id:
            partner_id = partner_id.parent_id
        # Montamos el warning para el comentario de cliente
        if partner_id.comment and partner_id.comment != "":
            title = ("Nota para %s") % partner_id.name
            message = "Nota cliente: %s" % partner_id.comment
            warning = {
                "title": title,
                "message": message,
            }
        # Montamos el warning para el comentario de administradores
        if (
            partner_id.admin_comment
            and partner_id.admin_comment != ""
            and self.is_comercial == False
        ):
            title = ("Nota para %s") % partner_id.name
            message = ""
            if partner_id.comment != "":
                message = """Nota cliente: %s
                            Nota de administrador: %s""" % (
                    partner_id.comment,
                    partner_id.admin_comment,
                )
            else:
                message = "Nota de administrador: %s" % partner_id.admin_comment

            warning = {
                "title": title,
                "message": message,
            }
        if warning:
            return {"warning": warning}

