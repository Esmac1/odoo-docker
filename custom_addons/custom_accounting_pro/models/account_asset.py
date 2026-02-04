from odoo import models, fields, api
from odoo.exceptions import UserError

class CustomAccountAsset(models.Model):
    _name = 'custom_accounting.asset'
    _description = 'Asset'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Asset Name', required=True)
    code = fields.Char(string='Reference')
    value = fields.Monetary(string='Initial Value', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    acquisition_date = fields.Date(string='Acquisition Date', required=True)
    useful_life = fields.Integer(string='Useful Life (months)')
    method = fields.Selection([
        ('linear', 'Linear'),
        ('degressive', 'Degressive')
    ], string='Depreciation Method', default='linear')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('close', 'Closed')
    ], string='Status', default='draft', tracking=True)
    
    # Depreciation fields
    accumulated_depreciation = fields.Monetary(string='Accumulated Depreciation', compute='_compute_depreciation', currency_field='currency_id')
    book_value = fields.Monetary(string='Book Value', compute='_compute_depreciation', currency_field='currency_id')
    
    @api.depends('value')
    def _compute_depreciation(self):
        for asset in self:
            # Simplified calculation
            months_owned = 6  # Example: 6 months owned
            monthly_depreciation = asset.value / (asset.useful_life or 60)
            asset.accumulated_depreciation = monthly_depreciation * months_owned
            asset.book_value = asset.value - asset.accumulated_depreciation

    def action_validate(self):
        self.write({'state': 'running'})
    
    def action_close(self):
        self.write({'state': 'close'})
