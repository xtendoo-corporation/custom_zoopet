from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPickingBatch(models.Model):
    _name = 'stock.picking.batch'
    _description = 'Lote de transferencias'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Batch Transfer', default='New',
        copy=False, required=True, readonly=True,
        help='Name of the batch transfer')

    user_id = fields.Many2one(
        'res.users', string='Responsable',
        tracking=True,
        default=lambda self: self.env.user
    )

    scheduled_date = fields.Datetime(
        'Fecha programada',
        copy=False,
        help="Fecha programada para las transferencias"
    )

    date_planned = fields.Datetime(
        'Fecha prevista',
        default=fields.Datetime.now,
        index=True,
        required=True
    )

    total_weight = fields.Float(
        compute='_compute_total_weight',
        string='Peso Total'
    )

    company_id = fields.Many2one(
        'res.company', string='Compañía', required=True, readonly=True,
        default=lambda self: self.env.company
    )

    picking_ids = fields.One2many(
        'stock.picking', 'batch_id', string='Transferencias',
        help='Lista de transferencias'
    )

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('in_progress', 'En progreso'),
        ('done', 'Validado'),
        ('cancel', 'Cancelado')],
        default='draft',
        store=True, tracking=True, copy=False
    )

    picking_type_id = fields.Many2one(
        'stock.picking.type', string='Tipo de operación'
    )

    move_ids = fields.One2many(
        'stock.move', compute='_compute_move_ids', string='Movimientos de stock'
    )

    allowed_picking_ids = fields.Many2many(
        'stock.picking', compute='_compute_allowed_picking_ids',
        string='Transferencias permitidas'
    )

    delivery_id = fields.Many2one(
        'delivery.carrier',
        string='Método de entrega'
    )

    @api.depends('picking_ids')
    def compute_total_weight(self):
        if not self.picking_ids:
            self.total_weight = 0.00
        for picking_id in self.picking_ids:
            if picking_id.weight != 0.00:
                self.total_weight += picking_id.weight

    def _sanity_check(self):
        """Verificar que los albaranes del lote son compatibles."""
        # Comprobar que no hay incompatibilidades entre los albaranes
        if not self.picking_ids:
            return

        # Verificar que todos los albaranes son del mismo tipo de operación
        picking_types = self.picking_ids.mapped('picking_type_id')
        if len(picking_types) > 1:
            raise UserError(_("No puedes mezclar albaranes de diferentes tipos de operación en el mismo lote."))

    move_line_ids = fields.One2many(
        'stock.move.line', compute='_compute_move_line_ids',
        string='Líneas de movimiento')

    @api.depends('picking_ids')
    def _compute_move_line_ids(self):
        for batch in self:
            # Obtener todas las líneas de movimiento asociadas a los albaranes del lote
            batch.move_line_ids = self.env['stock.move.line'].search([
                ('picking_id', 'in', batch.picking_ids.ids)
            ])

    show_check_availability = fields.Boolean(
        compute='_compute_show_check_availability',
        string='Mostrar comprobar disponibilidad')

    @api.depends('picking_ids', 'state')
    def _compute_show_check_availability(self):
        for batch in self:
            # El botón "Comprobar disponibilidad" se muestra cuando el lote está
            # en progreso y tiene albaranes que no están en estado 'done' o 'cancel'
            batch.show_check_availability = (
                batch.state == 'in_progress' and
                any(picking.state not in ('done', 'cancel') for picking in batch.picking_ids)
            )

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            # Intenta usar directamente la secuencia existente (ID 72)
            vals['name'] = self.env['ir.sequence'].browse(263).next_by_id()

            # Si no encuentra la secuencia por ID, busca por código
            if not vals['name'] or vals['name'] == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('stcok.picking.batch') or 'New'
        return super(StockPickingBatch, self).create(vals)

    @api.depends('picking_ids')
    def _compute_move_ids(self):
        for batch in self:
            batch.move_ids = batch.picking_ids.move_lines  # Cambiado de move_ids a move_lines

    @api.depends('picking_ids')
    def _compute_total_weight(self):
        for batch in self:
            weight = 0.0
            for picking in batch.picking_ids:
                if hasattr(picking, 'weight') and picking.weight:
                    weight += picking.weight
            batch.total_weight = weight

    @api.depends('company_id', 'state')
    def _compute_allowed_picking_ids(self):
        for batch in self:
            # Dominio que excluye albaranes asignados a OTROS lotes pero permite los del lote actual
            domain = [
                ('company_id', '=', batch.company_id.id),
                ('state', '!=', 'cancel'),
                '|',
                ('batch_id', '=', False),  # No asignados a ningún lote
                ('batch_id', '=', batch.id)  # O ya asignados a este mismo lote
            ]
            batch.allowed_picking_ids = self.env['stock.picking'].search(domain,limit=1)

    @api.model
    def _search_panel_domain_image(self, field_name, **kwargs):
        if field_name == 'picking_ids':
            # Filtrar automáticamente cuando se muestra el panel de búsqueda
            return [('batch_id', '=', False), ('state', '!=', 'cancel')]
        return super()._search_panel_domain_image(field_name, **kwargs)

    def action_confirm(self):
        self.write({'state': 'in_progress'})

    def action_assign(self):
        for picking in self.picking_ids:
            picking.action_assign()

    def action_done(self):
        for picking in self.picking_ids:
            if picking.state not in ['assigned', 'done']:
                raise UserError(_("No se puede validar el lote porque algunas transferencias no están disponibles."))
            picking.button_validate()
        self.write({'state': 'done'})

    def action_cancel(self):
        self.picking_ids.action_cancel()
        self.write({'state': 'cancel'})

    def action_draft(self):
        self.write({'state': 'draft'})
