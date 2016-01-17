from openerp import models, fields, api, osv
from datetime import datetime, date
import time

# To-do get method to return a list of defaulted id's using base method
class my_base_sred_object(models.Model):
    _name       = 'sred_system.base_sred_object'
    name        = fields.Char()

    @api.one
    def say(self, info):
        print "#######################"
        print info
        print "#######################"


class my_base_sred_picklist(models.Model):
    _name       = 'sred_system.base_sred_picklist'
    _inherit    = 'sred_system.base_sred_object'
    is_default  = fields.Boolean()
    is_internal = fields.Boolean()
    sequence    = fields.Integer()

    @api.one
    @api.model
    def _get_next_sequence(self):
        num_c = (len(self) + 1 ) * 10

    @api.one
    @api.model
    def get_default(self):
        # this_pool = self.env.search([('is_default','=',True)])[0]
        return []

    @api.one
    @api.model
    def get_pool(self, model_name, search_filter):
        return self.env[model_name].search(search_filter)


    _defaults = {'is_internal':False, 'is_default':False, 'sequence': 10}


class my_base_sred_task(models.Model):
    _name   = 'sred_system.base_sred_tasks'
    _inherit = 'sred_system.base_sred_picklist'

    # Override this to create child -- parent relationship
    task_id = fields.Integer()
    name    = fields.Char()

    sequence       = fields.Integer()
    date_deadline  = fields.Date()
    date_start     = fields.Date()
    date_end       = fields.Date()
    description    = fields.Html()
    assigned_to    = fields.Many2one('res.users', 'assigned person', ondelete='set null')
    completed      = fields.Boolean()

    _defaults={
 #     'journal_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
      'assigned_to': lambda s, cr, uid, c: uid
    }

