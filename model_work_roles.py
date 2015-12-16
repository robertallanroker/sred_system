from openerp import models, fields, api, osv
from datetime import datetime, date
import time

#
#                          /---| WORK_TYPES
#                         /
#   WORK_RESOURCE_ROLES >|-----| WORK_RESOURCE_SCOPE
#           V             \
#           |              \---| WORK_FUNCTIONS
#           |
#           |-----------> SRED_PROJECT
#
#

class my_work_functions(models.Model):
    _inherit = 'sred_system.base_sred_object'
    _name = 'sred_system.work_functions'
    work_function_id = fields.Many2many('sred_system.work_resource_roles', 'work_functions', 'work_function_id', string='work_functions')
    description = fields.Html()




# A Picklist of roles working types from db
class my_work_types(models.Model):
    _inherit = 'sred_system.base_sred_object'
    _name = 'sred_system.work_types'
    work_type_id = fields.Many2many('sred_system.work_resource_roles', 'work_types', 'work_type_id', string='work_types')
    description = fields.Html()



# A Picklist of role scopes from db
class my_scope(models.Model):
    _inherit = 'sred_system.base_sred_object'
    _name = 'sred_system.work_resource_scope'
    scope_id = fields.One2many('sred_system.work_resource_roles', 'work_resource_scope', string='scope')




# Journals all the roles assigned to a claim project
class my_work_resource_roles(models.Model):
    _name = 'sred_system.work_resource_roles'
#    name = fields.Char()  # not used

    work_types      = fields.Many2many('sred_system.work_types', 'work_type_id', 'work_types', string='work assignments')
    work_functions  = fields.Many2many('sred_system.work_functions', 'work_function_id', 'work_functions', string='work functions')
    work_person     = fields.Many2one('res.partner', string="Individual", ondelete='set null')
    work_role_id    = fields.Many2one('sred_system.sred_project', string='people assigned', ondelete='cascade')
    work_resource_scope = fields.Many2one('sred_system.work_resource_scope', string='scope', ondelete='cascade')

