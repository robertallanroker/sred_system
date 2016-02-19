# -*- coding: utf-8 -*-
{
    'name': "sred_system",

    'summary': """
        Makes many modifcations and updates to core system and
        implements a new module for an SRED Services provider.
        """,

    'description': """
        Green Light Inovations Partners has developed a new module that allows SRED,
        Service providers to manage work loads and collaborate easier with clients.
        We modify projects module so that specialized SRED tracking is in place which
        in turn allows new or existing odoo customers to receive eligable refunds from the
        Canadian government for thier RD efforts.
    """,

    'author': "Green Light Innovation Partnes",
    'website': "http://www.GreenLightIP.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Projects, SRED, Applications, Canada',

    'version': '3.0',
    'sequence': 11,

    # any module necessary for this one to work correctly
    'depends': ['web',
        'base',
        'base_setup',
        'project',
        'product',
        'mail',
        'analytic',
        'portal',
        'resource',
        'calendar',
        'google_calendar',
        'google_drive',
        'google_spreadsheet',
        'crm',
        'document',
        'analytic',
        'account',
        'account_accountant',
#        'board',
        'event',
#        'event_sale',
        'bus',
        'association',
        'gamification',
        'hr',
        'hr_recruitment',
        'hr_payroll',
        'hr_timesheet_sheet',
        'im_livechat',
        'marketing',
        'marketing_campaign',
        'mass_mailing',
        'link_tracker',
        'membership',
        'note',
#        'portal',
        'survey',
        'survey_crm',
        'subscription',
#        'warning',
#        'website_quote',
#        'website_blog',
#        'web_analytics',
#        'web_editor',
#        'web_kanban',
#        'web_view_editor',
#        'web_settings_dashboard',
#        'web_kanban_gauge',
#        'web_diagram',
        'website',
        'website_event',
        'website_google_map',
        'website_hr',
        'website_livechat',
        'website_mail',
        'website_mail_channel',
        'website_slides',
        'website_form',
        'website_forum',
        'website_blog',
#        'website_portal',
        'website_twitter',
        'website_forum_doc',
#        'web_diagram',
#        'portal_gamification',
#        'web_planner',
        "l10n_ca"],
     #   'web_planner',
     #   'calendar',],

    #'js': ['static/src/js/view_list.js'],

    # always loaded
    'data': [
        'load_data/load_data.xml',
        'views/sred_system.xml',
        'views/views.xml',
        'views/view_work_folders.xml',
        'views/view_sred_claim.xml',
        'views/reorganize.xml',
        'views/view_menus.xml',
        'reports/templates.xml',
        'security/ir.model.access.csv',
        'views/reorganize.xml',
        'views/mail_templates.xml',
        'views/mods_to_existing_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'load_demo_data/demo.xml',


    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}