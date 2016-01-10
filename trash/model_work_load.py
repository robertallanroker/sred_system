from openerp import models, fields, api, osv
from datetime import datetime, date
import calendar
import time


class my_sred_work_load(models.Model):
    _name = "sred_system.work_load"
    work_load_id = fields.Many2many('sred_system.sred_project','work_load_id','a_work_load', string='calendar of work load')
    work_event   = fields.Many2one('calendar.event', string="link to the calendar event", ondelete='set null')

