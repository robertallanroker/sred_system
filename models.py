# -*- coding: utf-8 -*-
from openerp import models, fields, api, osv
from datetime import datetime, date
import time

#
# MODIFICATIONS TO PROJECT ENTITIES
#

class my_uncertainties(models.Model):
    _name= 'sred_system.uncertainties'
    name = fields.Char()
    uncertainties_id = fields.Integer()
    description = fields.Char()

class my_hypothesis(models.Model):
    _name= 'sred_system.hypothesis'
    name = fields.Char()
    Is_Active = fields.Boolean()
    List_of_uncertainties = fields.Integer()

class my_milestones(models.Model):
    _name = 'sred_system.milestones'
    name = fields.Char()

class my_work_folders(models.Model):
    _inherit   = 'sred_system.base_sred_object'
    _name = 'sred_system.work_folders'
    name = fields.Char()
    num_sred_projects = fields.Integer()
    Folder_id = fields.One2many('sred_system.sred_project', 'an_assigned_folder', ondelete='cascade')
    Value_in_fees = fields.Float(string="Value Of Folder", compute='_compute_fees', store=False)
    is_active = fields.Boolean()
    _defaults = {'isactive':True}

    # Each work item will have a corresponding  sred claim project
    @api.one
    def _compute_fees(self):
        fee_amount = 0.00
        num_count = 0
        these_folders = []
        if self.Folder_id != []:
            for these_folders in self.Folder_id:
                fee_amount += these_folders.Estimated_Fee
                num_count = num_count + 1

        self.Value_in_fees = fee_amount
        self.num_sred_projects = num_count

## No need? Have Documentation Types now?
class my_ObjectiveEvidence_types(models.Model):
    _name = 'sred_system.objective_evidence_types'
    name = fields.Char()


class my_work_functions(models.Model):
    _inherit = 'sred_system.base_sred_object'
    _name = 'sred_system.work_functions'
    work_function_id = fields.Many2many('sred_system.work_roles', 'a_workfunctions', 'work_function_id', string='work_functions')
    description = fields.Html()

# A Picklist of roles working types from db
class my_work_types(models.Model):
    _inherit = 'sred_system.base_sred_object'
    _name = 'sred_system.work_types'
    work_type_id = fields.Many2many('sred_system.work_roles', 'a_work_types', 'work_type_id', string='work_types')
    description = fields.Html()

# A Picklist of role scopes from db
class my_scope(models.Model):
    _inherit = 'sred_system.base_sred_object'
    _name = 'sred_system.work_scope'
    scope_id = fields.One2many('sred_system.work_roles', 'work_resource_scope', string='scopeyscope')

# Journals all the roles assigned to a claim project
class my_work_roles(models.Model):
    _name = 'sred_system.work_roles'
    name = fields.Char()  # not used
    a_work_types      = fields.Many2many('sred_system.work_types', 'work_type_id', 'work_types', string='work assignments')
    a_work_functions  = fields.Many2many('sred_system.work_functions', 'work_function_id', 'work_functions', string='work functions')
 #   work_scope      = fields.Many2many('sred_system.scope', 'scope_id', 'work_scope')
    work_person     = fields.Many2one('res.partner', string="Individual", ondelete='set null')
    work_role_id    = fields.Many2one('sred_system.sred_project', string='people assigned', ondelete='cascade')

    work_resource_scope      = fields.Many2one('sred_system.work_scope', string='scope_of_me', ondelete='cascade')



