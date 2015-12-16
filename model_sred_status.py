from openerp import models, fields, api, osv
from datetime import datetime, date
import time

class my_sred_states(models.Model):
    _name       = 'sred_system.sred_states'
    name        = fields.Char()
    state_id    = fields.One2many('sred_system.sred_project','sred_state', string ='SRED Work States')
    sequence    = fields.Integer(default=10)
    is_default  = fields.Boolean(default=False)

class my_sred_working_status(models.Model):
    _name       = 'sred_system.sred_working_status'
    name        = fields.Char()
    working_status_id = fields.One2many('sred_system.sred_project','sred_working_status', string ='SRED Working Status')
    sequence    = fields.Integer(default=10)
    is_default  = fields.Boolean(default=False)

class my_sred_processing_status(models.Model):
    _name      = 'sred_system.sred_processing_status'
    name        = fields.Char()
    processing_status_id = fields.One2many('sred_system.sred_project','sred_processing_status', string='SRED Processing Status')
    sequence    = fields.Integer(default=10)
    is_default  = fields.Boolean(default=False)

class my_sred_cra_status(models.Model):
    _name      = 'sred_system.sred_cra_status'
    name        = fields.Char()
    cra_status_id = fields.One2many('sred_system.sred_project', 'sred_cra_status', string='SRED CRA Status')
    sequence    = fields.Integer(default=10)
    is_default  = fields.Boolean(default=False)
