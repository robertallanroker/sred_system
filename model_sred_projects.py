from openerp import models, fields, api, osv
from datetime import datetime, date
import time



class my_claim_types(models.Model):
    _name = 'sred_system.claim_types'
    _inherit = 'sred_system.base_sred_picklist'
    sred_id  = fields.One2many('sred_system.claim_project', 'claim_type', ondelete='cascade')




class my_estimations(models.Model):
    _name       = 'sred_system.work_estimations'
    estimate_id = fields.Many2one('sred_system.claim_project', string='Estimation', ondelete='cascade')
    e_date      = fields.Datetime()
    person      = fields.Many2one('res.users', string="person", ondelete='set null')
    refund      = fields.Float(digits=(10,2))
    fee         = fields.Float(digits=(10,2))

    _defaults={
      'e_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
      'person': lambda s, cr, uid, c: uid
    }








class my_sred_projects_tasks(models.Model):
    _name       = 'sred_system.sred_project_tasks'
    _inherit    = 'sred_system.base_sred_tasks'

    task_id = fields.Many2one('sred_system.claim_project', string='project', ondelete='set null')

    stage_type   = [('s1', 'Work'), ('s2','Greenlight'), ('s3', 'CRA'), ('s4', 'Claim-State')]
    stagetype    = fields.Selection(stage_type)

    stageme      = fields.Char(_compute='get_stage')

    processing_status = fields.Many2one('sred_system.processing_status', 'processing-queue',
                                        domain=[('stage', '=', 's2')],
                                        ondelete='set null')
    @api.one
    @api.model
    def relink_stage(self):
        self.stagetype = processing_status.stage

    @api.one
    @api.model
    def get_stage(self):
        self.stageme='s2'
        return ret


#
# MY_SRED_PROJECTS
#
class my_sred_projects(models.Model):
 #   _inherit        = ['project.project', 'mail.thread', 'ir.needaction_mixin']
 #   _inherit = ['project.project', 'mail.thread', 'ir.needaction_mixin']
    _inherit = ['sred_system.base_sred_object', 'mail.thread', 'ir.needaction_mixin']

 #    I would rather link to a new record relationship for now
 #   _inherits = {"mail.alias": "alias_id"}
    _name           = 'sred_system.claim_project'


    _period_number  = 5

    saved_company_logo = fields.Binary()

    ###########################################
    # MISSING FIELDS FROM PROJECT INHERITANCE #
    ###########################################
    #_alias#_models           = lambda self, *args, **kwargs: self._get_alias_models(*args, **kwargs)
    #_visibility_selection   = lambda self, *args, **kwargs: self._get_visibility_selection(*args, **kwargs)

    active                  = fields.Boolean('Active',
                                help ="If the active field is set to False, it will allow you to hide the project without removing it.")

    sequence                = fields.Integer('Sequence',
                                help = "Gives the sequence order when displaying a list of Projects.")

 #   analytic_account_id     = fields.Many2one('account.analytic.account', 'Contract/Analytic',
 #                               help    = "Link this project to an analytic account if you need financial management on projects. "
 #                                         "It enables you to connect projects with budgets, planning, cost and revenue analysis, timesheets on projects, etc.",
 #                               ondelete= "cascade",
 #                               required= True, auto_join=True)

 #   label_tasks             = fields.Char('Use Tasks as',
 #                               help    = "Gives label to tasks on project's kanban view.")

 #   resource_calendar_id    = fields.Many2one('resource.calendar', 'Working Time',
 #                               help    = "Timetable working hours to adjust the gantt diagram report", states={'close':[('readonly',True)]} )

 #   type_ids                = fields.Many2many('project.task.type', 'project_task_type_rel', 'project_id', 'type_id', 'Tasks Stages', states={'close':[('readonly',True)], 'cancelled':[('readonly',True)]})

 #   task_count              = fields.Integer(compute='_task_count', string  = "Tasks")

 #   task_needaction_count   = fields.Integer(compute='_task_needaction_count', string = "Tasks",)

    task_ids                = fields.One2many('sred_system.sred_project_tasks', 'task_id', "Task Items")

    color                   = fields.Integer('Color Index')

    user_id                 = fields.Many2one('res.users', 'Project Manager', track_visibility='onchange')

  #  alias_id                = fields.Many2one('mail.alias', 'Alias')

    partner_id              = fields.Many2one('res.partner','rel_to_company_from_sred_projects',
                                              domain=[('is_company', '=', True)],
                                              ondelete='set null')


#                                help    = "Internal email associated with this project. Incoming emails are automatically synchronized "
#                                                 "with Tasks (or optionally Issues if the Issue Tracker module is installed).")

  #  alias_model             = fields.Selection(_alias_models, "Alias Model", select=True, required=True,
  #                              help    = "The kind of document created when an email is received on this project's email alias")

#    privacy_visibility      = fields.Selection(_visibility_selection, 'Privacy / Visibility', required=True,
#                                help    = "Holds visibility of the tasks or issues that belong to the current project:\n"
#                                                "- Portal : employees see everything;\n"
#                                                "   if portal is activated, portal users see the tasks or issues followed by\n"
#                                                "   them or by someone of their company\n"
#                                                "- Employees Only: employees see all tasks or issues\n"
#                                                "- Followers Only: employees see only the followed tasks or issues; if portal\n"
#                                                "   is activated, portal users see the followed tasks or issues.")

#    state                   = fields.Selection([('draft','New'), ('open','In Progress'), ('cancelled', 'Cancelled'),
#                                             ('pending','Pending'), ('close','Closed')],
#                                                string='Status', required=True, copy=False)

#    doc_count               = fields.Integer(compute='_get_attached_docs', string="Number of documents attached")
#
    date_start              = fields.Date('Start Date')

    date                    = fields.Date('Expiration Date', select=True, track_visibility='onchange')

#    attachment_ids          = fields.One2many('ir.attachment', 'res_id', domain=lambda self: [('res_model', '=', self._name)], auto_join=True, string='Attachments')
    # In the domain of displayed_image_id, we couln't use attachment_ids because a one2many is represented as a list of commands so we used res_model & res_id
#    displayed_image_id      = fields.Many2one('ir.attachment', domain="[('res_model', '=', 'project.sred_project'), ('res_id', '=', id), ('mimetype', 'ilike', 'image')]", string='Displayed Image')

    attachment_ids          = fields.One2many('ir.attachment', 'res_id', string='Attachments')

    #######################
    # CLAIM STATUS FIELDS #
    #######################
    work_processing_status   = fields.Many2one('sred_system.processing_status',
                             string="work in progress",
                             ondelete='set null',
                             domain=[('stage', '=', 's1')],
                             track_visibility='onchange')

    glip_processing_status  = fields.Many2one('sred_system.processing_status',
                             string="Processing Status",
                             ondelete='set null',
                             domain=[('stage', '=', 's2')],
                             track_visibility='onchange')

    cra_processing_status = fields.Many2one('sred_system.processing_status',
                             string="CRA Status",
                             ondelete='set null',
                             domain=[('stage', '=', 's3')],
                             track_visibility='onchange')

    claim_status          = fields.Many2one('sred_system.processing_status',
                            string='claim Status',
                            ondelete='set null',
                            domain=[('stage', '=', 's4')],
                            track_visibility='onchange')


    ###################################
    # TRACK CLAIM ORGANIZATION FIELDS #
    ###################################
    folder_group            = fields.Many2one('sred_system.folder_groups', string='relation to folder group', ondelete='set null')
    folder                  = fields.Many2one('sred_system.work_folders',
                                  string="assigned folder",
                                  ondelete='cascade',
                                  track_visibility='on_change')

    claim_type               = fields.Many2one('sred_system.claim_types',
                                  string='claim type',
                                  ondelete='set null',
                                  track_visibility='on_change')

    tax_years               = fields.Many2many('sred_system.tax_years','taxyear_id','tax_years')

    work_started_on         = fields.Date()

    work_cra_deadline       = fields.Date()


    ####################
    # FINANCIAL FIELDS #
    ####################
    bin_number              = fields.Char()

    financial_year_end      = fields.Date()

    # Read only computed copies of the Estimated values
    # glitch in setting fields that requiring updating using views that are read-only turn fields into non-updatable
    # use the calculated fields instead on view forms to avoid the crazy glitch
    refund                  = fields.Float(compute='_calc_refund')

    fee                     = fields.Float(compute='_calc_fee')

    estimated_refund        = fields.Float()

    estimated_fee           = fields.Float()

    estimations             = fields.One2many('sred_system.work_estimations', 'estimate_id',
                                  string='Estimates',
                                  track_visibility='on_change')


    ###############################
    # ROLES AND LEADERSHIP FIELDS #
    ###############################
    technical_lead          = fields.Char()

    financial_lead          = fields.Char()

    work_roles              = fields.One2many('sred_system.work_roles', 'work_role_id',
                                   string='assignment of work roles', ondelete='cascade')


    #######################
    # TASK RELATED FIELDS #
    #######################


    ####################
    # ALL OTHER FIELDS #
    ####################
    notes = fields.Html('Notes')

    email_feed = fields.Char(compute='_calc_alias')


    ############################## M E T H O D S ##################################

#    def _auto_init(self, cr, context=None):
#        """ Installation hook: aliases, project.project """
#        # create aliases for all projects and avoid constraint errors
#        alias_context = dict(context, alias_model_name='sred_system.sred_project')
#        new_alias = self.pool.get('mail.alias').migrate_to_alias(cr, self._name, self._table, super(my_sred_projects, self)._auto_init,
#            'sred_system.sred_project', self._columns['alias_id'], 'id', alias_prefix='claim+', alias_defaults={'claim_id':'id'}, context=alias_context)#
#
#        self.alias_id = new_alias
#
#        return new_alias

 #   def create(self, cr, uid, vals, context=None):
 #$       if context is None:
 #           context = {}
 #       create_context = {}
#        ir_values = self.pool.get('ir.values').get_default(cr, uid, 'project.config.settings', 'generate_project_alias')
#        if ir_values:
#            vals['alias_name'] = vals.get('alias_name') or vals.get('name')

  #      new_id = super(my_sred_projects, self).create(cr, uid, vals, context=create_context)
  #      project_rec = self.browse(cr, uid, new_id, context=context)
#        project_rec.id = new_id.id
#        self.setup_alias(cr, uid, new_id, context=context)

 #       return new_id

   # @api.model
   # def create(self, vals):
   #     new_record = super(my_sred_projects, self).create(vals)
   #    self.setup_alias
   #     return new_record


    @api.one
    @api.model
    @api.onchange('partner_id')
    def _update_partner_logo(self):
        if self.partner_id.image:
            self.saved_company_logo = self.partner_id.image
        return

    @api.one
    @api.model
    def _calc_alias(self):
        feed_n = ""
 #       if self.alias_id:
 #           feed_n = self.alias_id.alias_name
        self.email_feed = feed_n
        return feed_n

    @api.one
    @api.model
    @api.depends('estimated_refund')
    def _calc_refund(self):
        self.refund = self.estimated_refund
        return self.estimated_refund

    @api.one
    @api.model
    @api.depends('estimated_fee')
    def _calc_fee(self):
        self.fee = self.estimated_fee
        return self.estimated_fee

    @api.model
    def _set_default_folder(self):
        my_folder_rec = []
        my_folder_id  = 0
        my_context = self.env.context
        if my_context:
            my_folder_id = my_context.get('my_folder_id')
            my_folder_rec = self.env['sred_system.work_folders'].browse(my_folder_id)
            if my_folder_rec:
                return my_folder_rec
        return my_folder_rec

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
    def _get_default_claim_type(self):
        new_record = []
        this_one = self.env['sred_system.claim_types'].search([('is_default','=',True)])
        if this_one:
            new_record = this_one[0]
        return new_record


    #  [('s1', 'Work'), ('s2','Greenlight'), ('s3', 'CRA'), ('s4', 'Claim-State')
    @api.model
    def _get_claim_status_default(self):
        new_record = []
        new_list = self.env['sred_system.processing_status'].search([('stage', '=', 's4'),
                                                                     ('is_default', '=', True)])
        if new_list:
            new_record = new_list[0]
        return new_record



    @api.model
    def _get_work_processing_status_default(self):
        new_record = []
        new_list   = self.env['sred_system.processing_status'].search([('stage', '=', 's1'), ('is_default', '=', True)])
        if new_list:
            new_record = new_list[0]
        return new_record


    @api.model
    def _get_glip_processing_status_default(self):
        new_record = []
        new_list   = self.env['sred_system.processing_status'].search([('stage', '=', 's2'), ('is_default', '=', True)])
        if new_list:
            new_record = new_list[0]
        return new_record


    @api.model
    def _get_cra_processing_status_default(self):
        new_record = []
        new_list   = self.env['sred_system.processing_status'].search([('stage', '=', 's3'), ('is_default', '=', True)])
        if new_list:
            new_record = new_list[0]
        return new_record


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

  #  @api.one
  #  @api.model
  #  def _set_default_tasks(self):
  #      this_data = self.env['sred_system.default_working_tasks'].search([('sequence','>=',0)])
  #      for this_rec in this_data:
  #         data_vals = {'name':this_rec.name,'project_id':self.id, 'user_id':self.user_id}
  #          this_new_record = self.env['sred_system.sred_project_tasks'].create(data_vals)
  #      self._say(this_data)
  #      self._say(this_new_list)
  #      return


    @api.one
    @api.onchange('estimations')
    def _calculate_claim(self):
        response = self._get_current_estimate()
        self.estimated_fee = response[0]
        self.estimated_refund = response[1]
        self._calc_fee
        self._calc_refund
        self._say(response[0])
        self._say(response[1])

        if self.folder:
           self.folder.calculate_fees()

    @api.one
    def open_claim(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sred_system.claim_project',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
        }


    @api.one
    @api.model
    def _make_new_alias(self):
 #       new_alias_dict = {'name':'new-alias','alias_parent_thread_id': self.id, 'alias_defaults': {'project_id': self.id}}
 #       new_alias_record = self.env['mail.alias']
 #       new_id = new_alias_record.create(new_alias_dict)
 #       this_project_record = self.env['sred_system.sred_project'].browse(self.id)
        return


    @api.one
    @api.model
    def open_project_claim(self):
        result = {
            "type": "ir.actions.act_window",
            "res_model": "sred_system.claim_project",
            "view_type": "form",
            "target": "current",
#            "domain": [('id', '=', claim_project_id)],
#            "context":
#            "context": context,
            "name": "SRED Project",
            "nodestroy": True}
        return result

    _order = "sequence, name, id"
    _defaults = {
        'active': True,
#        'type': 'contract',
#       'label_tasks': 'Tasks',
#       'state': 'open',
        'sequence': 10,
        'user_id': lambda self,cr,uid,ctx: uid,
#        'alias_model': 'project.task',
        'name': "New Claim",
        'tax_years': _get_tax_year_defaults,
        'claim_type': _get_default_claim_type,
        'claim_status': _get_claim_status_default,
        'work_processing_status': _get_work_processing_status_default,
        'glip_processing_status': _get_glip_processing_status_default,
        'cra_processing_status': _get_cra_processing_status_default,
#        'alias_id': _make_new_alias,
        'folder': _set_default_folder}