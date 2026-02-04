from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    total_overdue = fields.Monetary(compute='_compute_overdue')
    overdue_invoices = fields.One2many('account.move', compute='_compute_overdue')

    @api.depends('invoice_ids')
    def _compute_overdue(self):
        for partner in self:
            invoices = partner.invoice_ids.filtered(lambda i: i.state == 'posted' and i.payment_state in ['not_paid', 'partial'] and i.invoice_date_due < fields.Date.today())
            partner.overdue_invoices = invoices
            partner.total_overdue = sum(invoices.mapped('amount_residual'))
