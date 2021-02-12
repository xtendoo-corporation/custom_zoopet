# -- coding: utf-8 --

from odoo import api, models, fields


class AdministratorMixinRule(models.Model):
    _name = 'administrator.mixin.rule'
    _description = 'Administrator Mixin Rule'

    is_comercial = fields.Boolean(
        compute='_is_comercial',
        string="Is Comercial",
        default=lambda self: self._get_default_comercial()
    )

    @api.one
    def _is_comercial(self):
        self.is_comercial = self.env["res.users"].has_group(
                "zoopet_administration.comercial_group"
            )

    @api.model
    def _get_default_comercial(self):
        return self.env["res.users"].has_group(
                "zoopet_administration.comercial_group"
            )

    show_admin_notes = fields.Boolean(
        compute='_show_admin_notes',
        string="Show Admin Notes",
        default=lambda self: self._get_default_show_admin_notes()
    )

    @api.one
    def _show_admin_notes(self):
        self.show_admin_notes = self.env["res.users"].has_group(
                "res_partner_hide_internal_notes.view_partner_internal_notes"
            )

    @api.model
    def _get_default_show_admin_notes(self):
        return self.env["res.users"].has_group(
                "res_partner_hide_internal_notes.view_partner_internal_notes"
            )
