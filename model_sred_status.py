from openerp import models, fields, api, osv
from datetime import datetime, date
import time



class my_default_tasks(models.Model):
    _name       = 'sred_system.default_tasks'
    _inherit    = 'sred_system.base_sred_tasks'
    processing_status = fields.Many2one('sred_system.processing_status', ondelete='set null')


# PROCESSING STATUS
class my_sred_processing_status(models.Model):
    _name        = 'sred_system.processing_status'
    _inherit     = "sred_system.base_sred_picklist"
    name         = fields.Char()
    revenue_type = [('a1', 'New'), ('a2', 'Processed'), ('a3', 'Booked'), ('a4', 'Deferred'), ('a4', 'Lost')]
    stage_type   = [('s1', 'Work'), ('s2','Greenlight'), ('s3', 'CRA'), ('s4', 'Claim-State')]
    revenue      = fields.Selection(revenue_type)
    stage        = fields.Selection(stage_type)
    sred_claim   = fields.One2many('sred_system.claim_project','claim_status','sred_claim_rel', ondelete='cascade')
    default_tasks= fields.One2many('sred_system.default_tasks','processing_status','status_task_rel', ondelete='cascade')

    _default = {'revenue':'a1', 'stage_type':'s1'}




