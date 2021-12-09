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

    def _is_comercial(self):
        self.is_comercial = self.env["res.users"].has_group(
                "zoopet_administration.comercial_group"
            )

    def _get_default_comercial(self):
        return self.env["res.users"].has_group(
                "zoopet_administration.comercial_group"
            )

    show_admin_notes = fields.Boolean(
        compute='_show_admin_notes',
        string="Show Admin Notes",
        default=lambda self: self._get_default_show_admin_notes()
    )

    def _show_admin_notes(self):
        self.show_admin_notes = self.env["res.users"].has_group(
                "res_partner_hide_internal_notes.view_partner_internal_notes"
            )

    def _get_default_show_admin_notes(self):
        return self.env["res.users"].has_group(
                "res_partner_hide_internal_notes.view_partner_internal_notes"
            )

    permission_to_archive = fields.Boolean(
        compute='_permission_to_archive',
        string="Permission to archive",
        default=lambda self: self._get_permission_to_archive()
    )

    def _permission_to_archive(self):
        self.permission_to_archive = self.env["res.users"].has_group(
                "res_partner_hide_internal_notes.permission_to_archive"
            )

    def _get_permission_to_archive(self):
        return self.env["res.users"].has_group(
                "res_partner_hide_internal_notes.permission_to_archive"
            )

    print_all_formats = fields.Boolean(
        compute='_print_all_formats',
        string="Print all Formats",
        default=lambda self: self._get_print_all_formats()
    )

    def _print_all_formats(self):
        self.print_all_formats = self.env["res.users"].has_group(
                "zoopet_administration.print_all_formats"
            )

    def _get_print_all_formats(self):
        return self.env["res.users"].has_group(
                "zoopet_administration.print_all_formats"
            )
