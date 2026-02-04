from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def action_reconcile(self):
        """Reconcile selected lines"""
        self.ensure_one()
        return self.reconcile()
