from openerp import models, fields, api, osv
from datetime import datetime, date
import time

class my_journal_types(models.Model):
    _name = 'sred_system.work_journal_types'
    name = fields.Char()
    sequence = fields.Integer()
    journal_type_id = fields.One2many('sred_system.work_journal', 'journal_types', ondelete='cascade')


class my_work_journal(models.Model):
    _name = 'sred_system.work_journal'
    name = fields.Char()

    journal_types = fields.Many2one('sred_system.work_journal_types', string="journal types", ondelete='set null')
    journal_date = fields.Datetime()
    journal_person = fields.Many2one('res.users', string="person", ondelete='set null')
    journal_description = fields.Html()
    journal_sred_project = fields.Many2one('sred_system.sred_project', string='SRED Claim', ondelete='cascade')

    _defaults={
      'journal_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
      'journal_person': lambda s, cr, uid, c: uid
    }