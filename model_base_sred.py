from openerp import models, fields, api, osv
from random import randint
from datetime import datetime, date
import time

# To-do get method to return a list of defaulted id's using base method
class my_base_sred_object(models.Model):
    _name        = 'sred_system.base_sred_object'
    _file_prefix = 'X'

    name         = fields.Char()
    file_no      = fields.Char()
    active       = fields.Boolean()


    @api.model
    def create(self, values):
        this_id = super(my_base_sred_object, self).create(values)
        self.cleanup
        return this_id

    @api.model
    def cleanup(self):
        data_rec = self.env[self._name].search([('file_no','=', None)])
        if data_rec:
            for my_rec in data_rec:
                self.file_no = self.make_file_no
        return


    @api.model
    def code_generator(self, num):
        code_get = ''
        current_num = num
        flipval = True
        while (current_num > 0):
            f_int = (current_num / 10) * 10
            r_int = (current_num - f_int)

            if randint(0,999) > 700:
                r_int = randint(1,9)

            if randint(0,500) > 300:
                offset_val = randint(0, 27)
                r_int = (r_int + offset_val)

            current_num = (current_num / 10)
            flipval = not flipval

            if (r_int > 90) or (r_int < 65):
                r_int = randint(65, 90)

            if flipval and (randint(1, 100) > 25):
                code_get = code_get + str(r_int)
            else:
                code_get = code_get + chr(r_int)

        return code_get


    @api.model
    def make_file_no(self):
        count_rec = self.env[self._name].search_count([('active', '=', True)])
        rand_no   = randint(0, 999)
        ms        = int(time.time() * 1000)
        this_file_no = self._file_prefix + '.' + self.code_generator(count_rec) + '.' + self.code_generator(rand_no) + '.'+ self.code_generator(ms)
        self.say(this_file_no)
        return this_file_no

    _defaults = {'file_no': make_file_no, 'active': True}


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
    color_index = fields.Integer()
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

