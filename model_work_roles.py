from openerp import models, fields, api, osv
from datetime import datetime, date
import time
import logging

_logger = logging.getLogger('sred_system.work_roles')

#
#                          /---| WORK_TYPES
#                         /
#   WORK_RESOURCE_ROLES >|-----| WORK_RESOURCE_SCOPE
#           V             \
#           |              \---| WORK_FUNCTIONS
#           |
#           |-----------> CLAIM_PROJECT
#
#



#
# Journals all the roles assigned to a claim project
class my_work_resource_roles(models.Model):
    _inherit = 'sred_system.base_sred_object'
    _name = 'sred_system.work_roles'
    name = fields.Char()  # not used


    work_types     = fields.Many2many('sred_system.work_types', 'work_type_id', 'work_types', string='work assignments')
    work_functions  = fields.Many2many('sred_system.work_functions', 'work_function_id', 'work_functions', string='work functions')

    work_person     = fields.Many2one('res.partner', string="Individual", ondelete='set null')
    work_person_image = fields.Binary(related='work_person.image', string="person image")
    work_role_id    = fields.Many2one('sred_system.claim_project', string='people assigned', ondelete='cascade')
    work_scope      = fields.Many2one('sred_system.work_scope', string='scope', ondelete='cascade')


    @api.one
    @api.model
    def get_login_user_id(self):
        login_user_id = []
        if self.work_person:
            login_user_id = self.env['res.users'].browse(self.work_person.id).id
        self.work_userid = login_user_id
        return login_user_id

    @api.onchange('work_scope')
    def on_change_work_scope(self):

        res = {}
        filter = {}
        filter['work_person'] = [('is_company', '=', False)]

        if self.work_scope:
            # Green light / Internal
            if self.work_scope.scope_type == '1':
                filter['work_person'] = [('is_company', '=', False), ('parent_id', '=', 1)]
            # Customer
            elif self.work_scope.scope_type == '2':
                if self.work_role_id.partner_id:
                    filter['work_person'] = [('is_company', '=', False), ('parent_id', '=', self.work_role_id.partner_id.id)]
                else:
                    res['warning'] = {'title': 'No Customer Assigned', 'message': 'No Customer Assigned, can not retrieve users within'}
                    res['value'] = {'work_scope': self.env['sred_system.work_scope'].search([('scope_type','=','1')])[0].id}
            elif self.work_scope.scope_type == '3':
                cra_id = self.env['res.partner'].search([('name','=','Canada Revenue Agency')])[0].id
                if cra_id:
                    filter['work_person'] = [('is_company', '=', False), ('parent_id', '=', cra_id)]
                else:
                    res['warning'] = {'title': 'Missing Record', 'message': 'There is no Canada Revenue Agency Partner Record in the system'}
                    res['value'] = {'work_scope': self.env['sred_system.work_scope'].search([('scope_type','=','1')])[0].id}
            elif self.work_scope.scope_type in ['4','5','6']:
                cra_id = self.env['res.partner'].search([('name','=','Canada Revenue Agency' )])[0].id
                if not cra_id:
                    cra_id = 0
                if self.work_role_id.partner_id:
                    p_id = self.work_role_id.partner_id
                else:
                    p_id = 0
                filter['work_person'] = [('parent_id', '<>', cra_id), ('parent_id','<>', 1), ('parent_id','<>', p_id)]

        res['domain'] = filter
        _logger.info('on work roles changed')
        _logger.info(res)
        return res



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
    scope_type = fields.Selection([('1', 'Internal'), ('2', 'Customer'), ('3', 'CRA'), ('4','External'), ('5', 'Competitor'), ('6', 'Partner')])
    scope_id = fields.One2many('sred_system.work_roles', 'work_scope', string='scope')