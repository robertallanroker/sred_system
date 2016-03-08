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
        'base',                     ## Primary Base Libraries
        'base_setup',               ## Primary Base Setup
        'base_action_rule',
        'calendar',                 ## Everyone needs a calendar
        'project',                  ## Basic Project Management and Tasks
        'crm',
        'account',                  ## Accounting Core
        'account_accountant',
        'analytic',                 ## CRM wont work without Analytics
        'gamification',             ## Have fun with goals
        'google_calendar',          ## Google Calendar Integration - Very Buggy
        'google_drive',
        'mail',
        'resource',
        'document',
        'association',
        'hr',
        'hr_recruitment',
        'hr_payroll',
        'hr_timesheet_sheet',
        'marketing_campaign',
        'mass_mailing',
        'link_tracker',
        'membership',
        'survey',
        'survey_crm',
        'note',
        'portal',
#       'subscription',
        'web_analytics',
        'web_editor',
        'web_kanban',
        'web_settings_dashboard',
        'web_kanban_gauge',
        'web_diagram',
        'portal_gamification',
        'web_planner',
        'website',
        'website_google_map',
        'website_event',
        'website_hr',
        'website_livechat',
        'website_mail',
        'website_mail_channel',
        'website_slides',
        'website_blog',
        'website_form',
        'website_forum',
        'website_blog',
        'website_portal',
        'website_twitter',
        'website_forum_doc',
        'bus',                          ## Instant Messaging, send messages to other users
        'im_livechat',
        'l10n_multilang'],
    'data': [
        'views/reorganize.xml',
        'views/sred_system.xml',
        'views/views.xml',
        'views/view_work_folders.xml',
        'views/view_contracts.xml',
        'views/view_sred_claim.xml',
        'views/view_manifest.xml',
        'views/view_menus.xml',
        'reports/templates.xml',
        'views/mods_crm_leads.xml',
        'views/mods_res_partner.xml',
        'security/ir.model.access.csv',
        'data/load_data/data_processing_status.xml',
        'data/load_data/data_partner_groups.xml',
        'data/load_data/data_res_partner.xml',
        'data/load_data/load_data.xml',
        'data/load_data/data_contracts.xml',
        'data/load_data/data_manifest.xml',
        'data/load_data/load_data/data_cron_events.xml'
    ],
    # only loaded in demonstration mode
    'qweb': ['views/view_sred_claim.xml'],
    'demo': ['data/load_demo_data/demo.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}