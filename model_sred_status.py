from openerp import models, fields, api, osv
from datetime import datetime, date
import time

class my_sred_states(models.Model):
    _inherit   = 'sred_system.base_sred_object'
    _name       = 'sred_system.sred_states'
    state_id    = fields.One2many('sred_system.sred_project','sred_state', string ='SRED Work States')

class my_sred_working_status(models.Model):
    _inherit   = 'sred_system.base_sred_object'
    _name       = 'sred_system.sred_working_status'
    working_status_id = fields.One2many('sred_system.sred_project','sred_working_status', string ='SRED Working Status')

class my_sred_processing_status(models.Model):
    _inherit   = 'sred_system.base_sred_object'
    _name      = 'sred_system.sred_processing_status'
    processing_status_id = fields.One2many('sred_system.sred_project','sred_processing_status', string='SRED Processing Status')

class my_sred_cra_status(models.Model):
    _inherit   = 'sred_system.base_sred_object'
    _name      = 'sred_system.sred_cra_status'
    cra_status_id = fields.One2many('sred_system.sred_project', 'sred_cra_status', string='SRED CRA Status')
