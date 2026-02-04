{
    "name": "Custom Helpdesk",
    "version": "1.0",
    "category": "Services/Helpdesk",
    "summary": "Custom Helpdesk Module with Kanban, Tree, and Form Views",
    "description": "A minimal helpdesk module with stages, priority, SLA, and resolution tracking.",
    "author": "Your Name",
    "depends": ["base", "mail"],
    "data": [
        # Security
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",

        # Data (stages, tags, sample tickets)
        "data/helpdesk_stage_data.xml",
        "data/helpdesk_tag_data.xml",
        "data/helpdesk_data.xml",

        # Views (actions must be loaded before menus)
        "views/helpdesk_ticket_views.xml",
        "views/helpdesk_ticket_kanban.xml",
        "views/helpdesk_team_views.xml",
        "views/helpdesk_templates.xml",

        # Menu (last, after actions are defined)
        "views/helpdesk_menu.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
