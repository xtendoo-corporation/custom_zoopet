# -- coding: utf-8 --

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = ["sale.order", "administrator.mixin.rule"]
    _name = "sale.order"

    # Método que devuelve el warning si el cliente tiene algun tipo de notas
    @api.onchange("partner_id")
    def onchange_partner_id_warning(self):
        print("**************************Llamada al warings************************************")
        print(self.show_admin_notes)
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
        title = ("Nota para %s") % partner_id.name
        if partner_id.comment and partner_id.comment != "":
            message = "Nota cliente: %s" % partner_id.comment
            
        # Montamos el warning para el comentario de administradores
        if (self.show_admin_notes == True):
            if (
                partner_id.admin_comment
                and partner_id.admin_comment != ""
                ):
                    message = message + " \n "
                    message =message + "Nota de administrador: %s" % partner_id.admin_comment

        # Montamos el warning para la alerta de venta
        if (partner_id.sale_warn_msg and partner_id.sale_warn_msg != ""):
            message = message + " \n "
            message =message + "Alerta de Pedido : %s" % partner_id.sale_warn_msg
            
        #Guardamos los datos dentro de warning y lo devolvemos
        warning = {
                "title": title,
                "message": message,
            }
        if warning:
            return {"warning": warning}




