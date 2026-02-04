from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    batch_payment_id = fields.Many2one('account.batch.payment', string="Batch")
    mandate_id = fields.Many2one('account.payment.mandate', string="Mandate")
    check_number = fields.Char()
    check_date = fields.Date()
    check_status = fields.Selection([
        ('draft', 'Draft'), 
        ('printed', 'Printed'),
        ('issued', 'Issued'),
        ('cleared', 'Cleared'),
        ('void', 'Void')
    ], default='draft')

class AccountBatchPayment(models.Model):
    _name = 'account.batch.payment'
    _description = 'Batch Payment'

    name = fields.Char(required=True, default='/')
    journal_id = fields.Many2one('account.journal', required=True)
    payment_ids = fields.One2many('account.payment', 'batch_payment_id', string="Payments")
    total_amount = fields.Monetary(compute='_compute_total', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='journal_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'), 
        ('posted', 'Posted'),
        ('cancel', 'Cancelled')
    ], default='draft')

    @api.depends('payment_ids.amount')
    def _compute_total(self):
        for batch in self:
            batch.total_amount = sum(batch.payment_ids.mapped('amount'))

    def action_post(self):
        self.payment_ids.filtered(lambda p: p.state == 'draft').action_post()
        self.state = 'posted'

class AccountPaymentMandate(models.Model):
    _name = 'account.payment.mandate'
    _description = 'Payment Mandate'
    
    name = fields.Char(required=True, default=lambda self: self.env['ir.sequence'].next_by_code('account.payment.mandate'))
    partner_id = fields.Many2one('res.partner', required=True)
    bank_account_id = fields.Many2one('res.partner.bank', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('valid', 'Valid'),
        ('expired', 'Expired')
    ], default='draft')
    start_date = fields.Date()
    end_date = fields.Date()
