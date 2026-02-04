{
    'name': 'Custom Accounting Pro',
    'depends': ['account', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'data/account_data.xml',
        'data/ir_sequence_data.xml',

        'views/account_move_views.xml',
        'views/account_payment_views.xml',
        'views/account_asset_views.xml',
        'views/account_budget_views.xml',
        'views/menu_views.xml',

        'wizards/batch_payment_wizard.xml',
        'wizards/followup_wizard.xml',

        'reports/report_templates.xml',
        'reports/report_invoice_qr.xml',
        'reports/report_followup.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_accounting_pro/static/src/css/custom_accounting.css',
        ],
    },
    'installable': True,
    'application': False,
}
