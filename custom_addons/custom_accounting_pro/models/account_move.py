from odoo import models, fields, api
import qrcode
from io import BytesIO
import base64

class AccountMove(models.Model):
    _inherit = 'account.move'

    is_credit_note = fields.Boolean(compute='_compute_is_credit_note', store=True)
    amount_to_settle = fields.Monetary(compute='_compute_amount_to_settle', string="To Settle")
    storno_move_id = fields.Many2one('account.move', string="Storno Reversal")
    qr_code = fields.Char(compute='_compute_qr_code', string="QR Code")

    @api.depends('move_type')
    def _compute_is_credit_note(self):
        for move in self:
            move.is_credit_note = move.move_type in ('out_refund', 'in_refund')

    @api.depends('amount_residual', 'state')
    def _compute_amount_to_settle(self):
        for move in self:
            move.amount_to_settle = move.amount_residual if move.state == 'posted' else 0

    @api.depends('name', 'amount_total', 'currency_id')
    def _compute_qr_code(self):
        for move in self:
            if move.state != 'posted' or not move.name:
                move.qr_code = False
                continue
            data = f"INV:{move.name}|AMT:{move.amount_total}|CUR:{move.currency_id.name}"
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            move.qr_code = base64.b64encode(buffer.getvalue()).decode()

    def action_storno(self):
        self.ensure_one()
        storno = self.copy({
            'date': fields.Date.today(),
            'ref': f"STORNO: {self.name}",
            'move_type': self.move_type,
        })
        for line in storno.line_ids:
            line.debit, line.credit = line.credit, line.debit
        storno.action_post()
        self.storno_move_id = storno.id
        return storno
