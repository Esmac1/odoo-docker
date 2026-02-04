from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountBudget(models.Model):
    _name = 'account.budget'
    _description = 'Budget'
    
    name = fields.Char(string='Budget Name', required=True)
    date_from = fields.Date(string='From Date', required=True)
    date_to = fields.Date(string='To Date', required=True)
    line_ids = fields.One2many('account.budget.line', 'budget_id', string='Budget Lines')
    state = fields.Selection([
        ('draft', 'Draft'), 
        ('validated', 'Validated'),
        ('done', 'Done')
    ], string='Status', default='draft')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', store=True)
    total_budget = fields.Monetary(string='Total Budget', compute='_compute_totals', currency_field='currency_id')
    actual_spent = fields.Monetary(string='Actual Spent', compute='_compute_totals', currency_field='currency_id')
    
    @api.depends('line_ids.planned_amount', 'line_ids.actual_amount')
    def _compute_totals(self):
        for budget in self:
            budget.total_budget = sum(budget.line_ids.mapped('planned_amount'))
            budget.actual_spent = sum(budget.line_ids.mapped('actual_amount'))
    
    def action_validate(self):
        self.write({'state': 'validated'})
    
    def action_set_draft(self):
        self.write({'state': 'draft'})

class AccountBudgetLine(models.Model):
    _name = 'account.budget.line'
    _description = 'Budget Line'
    
    budget_id = fields.Many2one('account.budget', string='Budget', required=True, ondelete='cascade')
    account_id = fields.Many2one('account.account', string='Account', required=True, domain=[('deprecated', '=', False)])
    planned_amount = fields.Monetary(string='Planned Amount', required=True, currency_field='currency_id')
    actual_amount = fields.Monetary(string='Actual Amount', compute='_compute_actual_amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='budget_id.currency_id', store=True)
    
    @api.depends('account_id', 'budget_id.date_from', 'budget_id.date_to')
    def _compute_actual_amount(self):
        for line in self:
            if not line.account_id or not line.budget_id.date_from:
                line.actual_amount = 0
                continue
            
            # Calculate actual amount from account moves in budget period
            moves = self.env['account.move.line'].search([
                ('account_id', '=', line.account_id.id),
                ('date', '>=', line.budget_id.date_from),
                ('date', '<=', line.budget_id.date_to),
                ('parent_state', '=', 'posted')
            ])
            line.actual_amount = abs(sum(moves.mapped('balance')))
