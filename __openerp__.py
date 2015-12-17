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

    'version': '0.5',
    'sequence': 11,

    # any module necessary for this one to work correctly
    'depends': ['base',
        'project',
        'base_setup',
        'product',
        'analytic',
        'mail',
        'portal',
        'resource',
        'web_kanban',
        'web_tip',
        'web_planner',
        'calendar'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/view_work_folders.xml',
        'views/view_work_load.xml',
        'views/view_sred_claim.xml',
        'views/view_work_journal.xml',
        'views/view_menus.xml',
        'reports/templates.xml',
        'load_data/load_folder_data.xml',
        'load_data/load_work_types_data.xml',
        'load_data/load_sred_projects_data.xml',
        'load_data/load_journal_types_data.xml',
        'load_data/load_work_resources.xml',
        'load_data/load_sred_states.xml',
        'load_data/load_documentation.xml',
        'load_data/load_cra_processing_states.xml',
        'security/ir.model.access.csv'
    ],
    # only loaded in demonstration mode
    'demo': [
        'load_demo_data/demo.xml',


    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}