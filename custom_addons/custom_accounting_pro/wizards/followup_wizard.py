from odoo import models, fields, api
from odoo.exceptions import UserError

class FollowupWizard(models.TransientModel):
    _name = 'account.followup.wizard'
    _description = 'Follow-up Wizard'
    
    partner_ids = fields.Many2many('res.partner', string='Customers', required=True,
                                  domain=[('customer_rank', '>', 0)])
    followup_type = fields.Selection([
        ('email', 'Email'),
        ('letter', 'Letter'),
        ('phone', 'Phone Call')
    ], string='Follow-up Type', default='email', required=True)
    template_id = fields.Many2one('mail.template', string='Email Template')
    subject = fields.Char(string='Subject')
    body = fields.Html(string='Message')
    overdue_invoices_only = fields.Boolean(string='Overdue Invoices Only', default=True)
    
    def action_send_followup(self):
        self.ensure_one()
        if not self.partner_ids:
            raise UserError("Please select at least one customer.")
        
        # Implementation for sending follow-ups
        for partner in self.partner_ids:
            # Find overdue invoices
            domain = [
                ('partner_id', '=', partner.id),
                ('state', '=', 'posted'),
                ('payment_state', 'in', ['not_paid', 'partial']),
                ('move_type', '=', 'out_invoice')
            ]
            if self.overdue_invoices_only:
                domain.append(('invoice_date_due', '<', fields.Date.today()))
            
            invoices = self.env['account.move'].search(domain)
            
            if invoices:
                # Here you would implement the actual follow-up sending logic
                # For now, we'll just create an activity
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'summary': f'Follow-up: {self.followup_type}',
                    'note': self.body or f'Follow up with {partner.name} regarding overdue invoices',
                    'user_id': self.env.user.id,
                    'res_id': partner.id,
                    'res_model_id': self.env.ref('base.model_res_partner').id,
                })
        
        return {
            'type': 'ir.actions.act_window_close'
        }
