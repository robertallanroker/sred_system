from openerp import models, fields, api, osv
from datetime import datetime, date
import time

class my_estimations(models.Model):
    _name = 'sred_system.work_estimations'
    estimate_id = fields.Many2one('sred_system.sred_project', string='Estimation', ondelete='cascade')
    e_date   = fields.Datetime()
    person = fields.Many2one('res.users', string="person", ondelete='set null')
    refund = fields.Float(digits=(10,2))
    fee    = fields.Float(digits=(10,2))

    _defaults={
      'e_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
      'person': lambda s, cr, uid, c: uid
    }

class my_sred_tax_years(models.Model):
    _inherit   = 'sred_system.base_sred_object'
    _name = 'sred_system.tax_years'
    name = fields.Char()
    taxyear_id = fields.Many2many('sred_system.tax_years','tax_years','taxyear_id')

# To-do, log date changes, keep running status changes
class status_dates(models.Model):
    _inherit   = 'sred_system.base_sred_object'
    _name = 'sred_system.sred_project'


class my_work_progress(models.Model):
    _name = 'sred_system.work_progress'

    status_label = fields.Char()
    started = fields.Datetime()
    eta     = fields.Datetime()
    stoped  = fields.Datetime()

    @api.model
    def _get_dt(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')

    @api.model
    def log_start(self, sred_project, status_label):
        return

    def log_stop(self, sred_project, status_label):
        return

class my_sred_type(models.Model):
    _name   = 'sred_system.sred_type'
    name    = fields.Char()
    is_default = fields.Boolean()
    sequence   = fields.Integer()
    sred_type_id = fields.One2many('sred_system.sred_project','work_types',string="Type of work", ondelete='cascade')

#
# MY_SRED_FINANCIAL_YEAR
# Structure used by other classes to contain a new financial year end field used in accounting and SRED claims processing
#
class my_sred_financial_year(models.Model):
    _name = 'sred_system.sred_financial_year'
    many_months = [('aJan','Jan'),('aFeb','Feb'), ('aMar','Mar'), ('aApr','Apr'),
              ('aMay','May'), ('aJune','June'),('aJuly','July'),
              ('aAug','Aug'),('aSep','Sep'),('aOct','Oct'),
              ('aNov','Nov'),('aDec','Dec')]
    financial_year_end_mm = fields.Selection(many_months)
    financial_year_end_dd = fields.Integer()

#
# MY_SRED_PROJECTS
#
class my_sred_projects(models.Model):
    _name        = 'sred_system.sred_project'
    _inherit     = ["mail.thread", "ir.needaction_mixin", "sred_system.sred_financial_year"]
    name         = fields.Char()

    bin_number = fields.Char()

    work_types  = fields.Many2one('sred_system.sred_type', string='work type', ondelete='set null')

    # ORGANIZATION INTO FOLDERS
    an_assigned_folder = fields.Many2one('sred_system.work_folders', string="assigned folder", ondelete='cascade')

    documentation = fields.Many2many('sred_system.documentation','sred_project', 'documentation', ondelete='cascade')

    # VARIOUS CLAIM STATUS
    #  New, Open, Closed, Etc...
#    project_type            = fields.Many2one('sred_system.project_types', string='project types', ondelete='set null')
    sred_state              = fields.Many2one('sred_system.sred_states', string="assigned_states", ondelete='set null')
    sred_working_status     = fields.Many2one('sred_system.sred_working_status', string="work in progress", ondelete='set null')
    sred_processing_status  = fields.Many2one('sred_system.sred_processing_status', string="Processing Status", ondelete='set null')
    sred_cra_status         = fields.Many2one('sred_system.sred_cra_status', string="CRA Status", ondelete='set null')

    # These should only be assigned onchange of relevant work roles
    current_technical_lead       = fields.Many2one('res.partner', string="Technical Lead", ondelete='set null')
    current_financial_lead       = fields.Many2one('res.partner', string="Financial Lead", ondelete='set null')

    a_claim_project = fields.Many2one('project.project', string="Claim Work Project", ondelete='set null')
    a_work_journal = fields.One2many('sred_system.work_journal','journal_sred_project', string ='Work Journal')

    a_list_of_sred_projects = fields.Many2one('project.project', string='List of eligable SRED project', ondelete='cascade')
    a_work_load = fields.Many2many('sred_system.work_load','a_work_load','work_load_id', string='calendar of work')

    customer = fields.Many2one('res.partner', string="Customer", ondelete='set null')

    # This will go away soon, these are either linked tasks, or events dates on status, or both.
    Work_Commenced = fields.Date()
    Work_Submitted = fields.Date()
    RC59_Submitted = fields.Date()
    CRA_Deadline = fields.Date()

    Notes = fields.Html('Notes')
    a_work_roles = fields.One2many('sred_system.work_resource_roles', 'work_role_id', string='assignment of work roles')

    Estimated_Refund = fields.Float(digits=(10,2), help = "123")
    Estimated_Fee    = fields.Float(digits=(10,2), help = "123")


    estimations = fields.One2many('sred_system.work_estimations', 'estimate_id', string='Estimates')

    tax_years = fields.Many2many('sred_system.tax_years','taxyear_id','tax_years')


    @api.model
    def create(self, values):
        new_id = super(my_sred_projects, self).create(values)
        return new_id

    @api.model
    def _set_default_folder(self):
        my_folder_rec = []
        my_folder_id  = 0
        my_context = self.env.context
        self.say(self.env)
        self.say(self._context)
        self.say('inside set default folder')
        self.say(my_context)
        if my_context:
            self.say('inside my_contect *if*')
            my_folder_id = my_context.get('my_folder_id')
            self.say(my_folder_id)
            my_folder_rec = self.env['sred_system.work_folders'].browse(my_folder_id)
            if my_folder_rec:
                self.say('found folder value')
                return my_folder_rec
        return my_folder_rec



#   @api.onchange('estimations')
    def _update_fees(self):
        my_rec = []
        for my_rec in self.estimations:
            self.Estimated_Refund = my_rec['refund']
            self.Estimated_Fee = my_rec['fee']


    # say()
    # I used this s/r to display debug messages onto the terminal window
    #
    @api.model
    def say(self, info):
        print "#########################################"
        if not info:
            info = "--Nothing--"
        print info
        print "#########################################"


    #
    # _get_tax_year_defaults()
    # tax_years is a table picklist of SR&ED claim years that can be associated to a work file.
    # this s/r pre-populate the list based on a boolean set value that the user can change.
    #
    @api.model
    def _get_tax_year_defaults(self):
        my_rec = []
        my_list = []
        my_list = self.env['sred_system.tax_years'].search([('is_default','=',True)]).ids
        return my_list

    @api.model
    def _get_sred_state_default(self):
        return self.env['sred_system.sred_states'].search([('is_default','=',True)])[0]

    @api.model
    def _get_working_status_default(self):
        return self.env['sred_system.sred_working_status'].search([('is_default','=',True)])[0]

    @api.model
    def _get_processing_status_default(self):
        return self.env['sred_system.sred_processing_status'].search([('is_default','=',True)])[0]

    @api.model
    def _get_cra_status_default(self):
        return self.env['sred_system.sred_cra_status'].search([('is_default','=',True)])[0]

    @api.model
    def _get_project_type_default(self):
        return self.env['sred_system.project_types'].search([('is_default','=',True)])[0]

    @api.model
    def _get_project_default(self):
        dval = {'name':"New Project"}
        my_rec = self.env['project.project'].create(dval)
        return my_rec

    @api.one
    @api.onchange('name')
    def _name_has_changed(self):
       self.say('on name change')
       self.a_claim_project.name= self.name


    @api.one
    def _get_current_fee_value(self):
        fee_amount  = 0.00
        if self.estimations:
            for my_rec in self.estimations:
                fee_amount = my_rec['fee']
        return fee_amount

    @api.one
    def _get_current_refund_value(self):
        refund_amount  = 0.00
        if self.estimations:
            for my_rec in self.estimations:
                refund_amount = my_rec['refund']
        return refund_amount


    @api.model
    def _get_current_estimate(self):
        answer = []
        fee_amount = 0.00
        refund_amount = 0.00
        found_one = False
        if self.estimations:
            for my_rec in self.estimations:
                if (my_rec['fee'] + my_rec['refund']) > 0:
                    if found_one == False:
                        fee_amount = my_rec['fee']
                        refund_amount = my_rec['refund']
                        last_entry = my_rec['e_date']
                        found_one = True
                    if found_one == True:
                        if last_entry < my_rec['e_date']:
                            fee_amount = my_rec['fee']
                            refund_amount = my_rec['refund']
                            last_entry = my_rec['e_date']
        answer.append(fee_amount)
        answer.append(refund_amount)
        return answer



    @api.one
    @api.onchange('estimations')
    def _calculate_claim(self):
        response = self._get_current_estimate()
        self.say(response[0])
        self.say(response[1])
        self.Estimated_Fee = response[0]
        self.Estimated_Refund = response[1]
        if self.an_assigned_folder:
            self.an_assigned_folder.calculate_fees()

    @api.one
    def open_claim(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sred_system.sred_project',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
        }

    @api.one
    @api.model
    @api.onchange('sred_state')
    def on_status_changed(self):
       self.message_post('testing')



    _defaults = {'tax_years': _get_tax_year_defaults,
                 'sred_state': _get_sred_state_default,
                 'sred_working_status': _get_working_status_default,
                 'sred_processing_status': _get_processing_status_default,
                 'sred_cra_status': _get_cra_status_default,
                 'a_claim_project': _get_project_default,
                 'project_type': _get_project_type_default,
                 'an_assigned_folder': _set_default_folder}

