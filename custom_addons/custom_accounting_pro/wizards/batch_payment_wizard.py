from odoo import models, fields, api
from odoo.exceptions import UserError

class BatchPaymentWizard(models.TransientModel):
    _name = 'account.batch.payment.wizard'
    _description = 'Batch Payment Wizard'
    
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, 
                                domain=[('type', 'in', ['bank', 'cash'])])
    payment_ids = fields.Many2many('account.payment', string='Payments', 
                                  domain=[('state', '=', 'draft'), ('payment_type', '=', 'outbound')])
    
    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        context = self._context
        if context.get('active_model') == 'account.payment' and context.get('active_ids'):
            res['payment_ids'] = [(6, 0, context.get('active_ids'))]
        return res
    
    def action_create_batch(self):
        self.ensure_one()
        if not self.payment_ids:
            raise UserError("Please select at least one payment.")
        
        # Create batch payment
        batch = self.env['account.batch.payment'].create({
            'name': self.env['ir.sequence'].next_by_code('account.batch.payment'),
            'journal_id': self.journal_id.id,
            'payment_ids': [(6, 0, self.payment_ids.ids)],
        })
        
        # Return action to open the created batch
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.batch.payment',
            'res_id': batch.id,
            'view_mode': 'form',
            'target': 'current',
        }
