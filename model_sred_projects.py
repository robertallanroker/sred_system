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


class my_documentation_labels(models.Model):
    _inherit   = 'sred_system.base_sred_object'
    _name = 'sred_system.documentation_labels'
    name = fields.Char()
    doc_label_id = fields.Many2many('sred_system.documentation', 'document_id', 'doc_label_id')


class my_documentation(models.Model):
    _inherit   = 'sred_system.base_sred_object'
    _name = 'sred_system.documentation'
    name = fields.Char()
    document_id = fields.Many2many('sred_system.documentation_labels', 'doc_label_id', 'document_id')
    document_tags = fields.Many2many('sred_system.documentation_tags', 'doctags_id', 'document_tags')
    sred_project = fields.Many2many('sred_system.sred_project', 'documentation', 'sred_project')

class my_documentation_tags(models.Model):
    _inherit   = 'sred_system.base_sred_object'
    _name = 'sred_system.documentation_tags'
    name = fields.Char()
    doc_tags_id = fields.Many2many('sred_system.documentation','document_tags', 'doc_tags_id')

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

#class my_sred_project_type(models.Model):
#    _inherit = 'sred_system.base_sred_object'
#    _name = 'sred_system.project_types'
#    project_type_id = fields.One2many('sred_system.sred_project', 'project_type', string='project work types', ondelete = 'cascade')


class my_sred_projects(models.Model):
    _name        = 'sred_system.sred_project'
    _inherit     = ["mail.thread", "ir.needaction_mixin"]
    name         = fields.Char()

    bin_number = fields.Char()
    financial_year_end_mm = fields.Integer()
    financial_year_end_dd = fields.Integer()

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

    Estimated_Due = fields.Date()
    Elapsed_Days  = fields.Char()

    tax_years = fields.Many2many('sred_system.tax_years','taxyear_id','tax_years')


    @api.model
    def create(self, values):
        new_id = super(my_sred_projects, self).create(values)
        print "inside create !!!!!"
        return new_id


    @api.model
    def set_default_project(self):
        my_record = []
        my_object = []
        dval = {
           'name': 'My Brother',
           'active': True,
           'sequence': 100}
        return

    @api.onchange('estimations')
    def _update_fees(self):
        my_rec = []
        for my_rec in self.estimations:
            self.Estimated_Refund = my_rec['refund']
            self.Estimated_Fee = my_rec['fee']

    @api.model
    def say(self, info):
        print "#########################################"
        print info
        print "#########################################"


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
        self.say("CREATING")
        return my_rec

    @api.onchange('name')
    def _name_has_changed(self):
       self.a_claim_project['name'] = "test"

    _defaults = {'tax_years': _get_tax_year_defaults,
                 'sred_state': _get_sred_state_default,
                 'sred_working_status': _get_working_status_default,
                 'sred_processing_status': _get_processing_status_default,
                 'sred_cra_status': _get_cra_status_default,
                 'a_claim_project': _get_project_default,
                 'project_type': _get_project_type_default}