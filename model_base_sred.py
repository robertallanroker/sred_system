from openerp import models, fields, api, osv
from datetime import datetime, date
import time

# To-do get method to return a list of defaulted id's using base method
class my_base_sred_object(models.Model):
    _name       = 'sred_system.base_sred_object'
    name        = fields.Char()
    is_default  = fields.Boolean()
    is_internal = fields.Boolean()
    sequence    = fields.Integer()
    _defaults   = {'is_default':False,
                   'is_internal':False,
                   'sequence':  10}