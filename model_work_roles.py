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




# Journals all the roles assigned to a claim project
class my_work_resource_roles(models.Model):
    _name = 'sred_system.work_roles'
    name = fields.Char()  # not used
#    name = fields.Char()  # not used

    work_types     = fields.Many2many('sred_system.work_types', 'work_type_id', 'work_types', string='work assignments')
    work_functions  = fields.Many2many('sred_system.work_functions', 'work_function_id', 'work_functions', string='work functions rel')
    work_person     = fields.Many2one('res.partner', string="Individual", ondelete='set null')
    work_person_image = fields.Binary(related='work_person.image', string="person image")
    work_role_id    = fields.Many2one('sred_system.claim_project', string='people assigned', ondelete='cascade')
    work_scope      = fields.Many2one('sred_system.work_scope', string='scope', ondelete='cascade')


class my_work_base_object(models.Model):
    _name = 'sred_system.base_roles_object'
    _inherit = 'sred_system.base_sred_picklist'
    is_internal = fields.Boolean()

    _defaults = {'is_internal':False}



class my_work_functions(models.Model):
    _name = 'sred_system.work_functions'
    _inherit = 'sred_system.base_roles_object'
    name = fields.Char()
    work_function_id = fields.Many2many('sred_system.work_roles', 'work_functions', 'work_function_id', string='work functions rel')
    description = fields.Html()


# A Picklist of roles working types from db
class my_work_types(models.Model):
    _name = 'sred_system.work_types'
    _inherit = 'sred_system.base_roles_object'
    name = fields.Char()
    work_type_id = fields.Many2many('sred_system.work_roles', 'work_types', 'work_type_id', string='work_types')
    description = fields.Html()


# A Picklist of role scopes from db
class my_scope(models.Model):
    _name = 'sred_system.work_scope'
    _inherit = 'sred_system.base_roles_object'
    name = fields.Char()
    scope_id = fields.One2many('sred_system.work_roles', 'work_scope', string='scope')