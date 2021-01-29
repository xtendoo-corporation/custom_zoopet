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
        message = ""
        partner_id = self.partner_id
        title = ("Nota para %s") % partner_id.name
        # Montamos el warning para el comentario de cliente
        if partner_id.comment != "":
            message = "Nota cliente: %s" % partner_id.comment
            
        # Montamos el warning para el comentario de administradores
        if self.show_admin_notes and partner_id.admin_comment != "":        
            message = message + " \n Nota de administrador: %s" % partner_id.admin_comment

        # Montamos el warning para la alerta de venta
        if partner_id.sale_warn in ['warning','block'] and partner_id.sale_warn_msg != "":
            message = message + " \n Alerta de Pedido : %s" % partner_id.sale_warn_msg
            
        #Si Se rellena message, se devuelve el warning
        if message != "":
            return {"warning":  {"title": title,
                                "message": message,
                                }
                    }




