from openerp import models, fields, api
from random import randint
import time
import logging
from openerp.tools.translate import _



_logger = logging.getLogger('sred_system.claim_projects')



class my_claim_types(models.Model):
    _name = 'sred_system.claim_types'
    _inherit = 'sred_system.base_sred_picklist'
    sred_id  = fields.One2many('sred_system.claim_project', 'claim_type', ondelete='cascade')


# sred_system.work_estimations
# Each claim project has a running list of estimations made since the beginning of the claim,
# and soon this will be part of this will also include since the beginning of a sales opportunity
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



# sred_system.sred_project_tasks
# We should change this to use the system's tasks. This version is used to track tasks, 
# CUrrently if we inherit from project.tasks, we need to disable functionality which currently ties
# the data to a project table. We want tasks in this case to tie directly to the claim_project
class my_sred_projects_tasks(models.Model):
    _name       = 'sred_system.sred_project_tasks'
    _inherit    = ['sred_system.base_sred_tasks', 'mail.thread', 'ir.needaction_mixin']
    _description = 'sred claim project tasks'

    task_id = fields.Many2one('sred_system.claim_project', string='project', ondelete='set null')

    stage_type   = [('s1', 'Work'), ('s2','Greenlight'), ('s3', 'CRA'), ('s4', 'Claim-State')]
    stagetype    = fields.Selection(stage_type)

    stageme      = fields.Char(_compute='get_stage')

    processing_status = fields.Many2one('sred_system.processing_status', 'processing-queue',
                                        domain=[('stage', '=', 's2')],
                                        ondelete='set null')

    partner_id    = fields.Many2one(related='task_id.partner_id')


    company = fields.Char(compute="_compute_company")

    @api.one
    def _compute_company(self):
        if self.task_id.partner_id:
            self.company = self.task_id.partner_id.name
        else:
            self.company = 'not assigned'
        return


    @api.one
    @api.model
    def relink_stage(self):
        self.stagetype = self.processing_status.stage

    @api.one
    @api.model
    def get_stage(self):
        self.stageme='s2'
        return


# sred_system.emails.
# This is crazy work-around. An alias email has to create a new record.  Hence if we want to see in the discussion thread,
# email's sent in, the alias will create the email thread. I've then added a CRON event that polls the email queue, and 
# changes the message attributes so that it can be seen inside the claim project.
# this works, however, there is about a 15 minute CRON polling delay
class my_sred_emails(models.Model):
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _name = 'sred_system.emails'
    _description = 'Track SRED related email'

    claim_project  = fields.Many2one('sred_system.claim_project', string='Claim Project')
    date_received  = fields.Datetime()
    trigger_update = fields.Boolean()
    last_email_id  = fields.Integer()

    @api.model
    @api.onchange('trigger_update')
    def on_change_from_new_email(self):
        print '*** TRIGGER UPDATE ****'
        return

    @api.model
    def run_fix_emails(self):
        _logger.info('Fixing Email Correspondence ...')
        mail_subtype    = self.env['mail.message.subtype'].search([('name','=','Note')])
        emails_to_fix = self.env['mail.message'].search([('model','=','sred_system.emails')])
        if emails_to_fix:
            for fix_this_one in emails_to_fix:
                _logger.info('Fix ')
                fix_this_one.model  = 'sred_system.claim_project'
                old_res_id = fix_this_one.res_id
                sred_email = self.env['sred_system.emails'].browse(old_res_id)[0]
                if sred_email:
                    fix_this_one.res_id = sred_email.claim_project.id
                if mail_subtype:
                    fix_this_one.subtype_id = mail_subtype
        else:
            _logger.info('Nothing to fix ...')

        return


    _defaults = {'trigger_update':False}

#
# MY_SRED_PROJECTS
#
class my_sred_projects(models.Model):
    _inherit = ['sred_system.base_sred_object','mail.thread', 'ir.needaction_mixin']
    _name           = 'sred_system.claim_project'
    _description    = 'sred claim project'
    _file_prefix    = 'CP'


    name            = fields.Char(required=True)
    sequence        = fields.Integer()

    website = fields.Char(related='partner_id.website')

    task_ids                = fields.One2many('sred_system.sred_project_tasks', 'task_id', "Task Items", track_visibility='onchange')

    user_id                 = fields.Many2one('res.users', 'Project Manager', track_visibility='onchange')
    user_image              = fields.Binary(string='user image', related='user_id.image')

    alias_id                = fields.Many2one('mail.alias', 'Alias')
    partner_id              = fields.Many2one('res.partner', 'rel_to_company_from_sred_projects', required=True,
                                              domain=[('customer', '=', True)])
    partner_name            = fields.Char(related='partner_id.name')

    contracted_service = fields.Many2one('sred_system.sred_contracts', string='contract label', required=True)
    contract_no        = fields.Char(related='contracted_service.file_no', string = 'Contract#')

    saved_company_logo      = fields.Binary(string='company logo', related='partner_id.image')

    date_start              = fields.Date('Start Date')

    date                    = fields.Date('Expiration Date', select=True, track_visibility='onchange')

#    attachment_ids          = fields.One2many('ir.attachment', 'res_id', string='Attachments')

    claim_file      = fields.Char(related='alias_id.display_name', readonly=True)
    cra_year_end    = fields.Datetime(related='partner_id.cra_year_end')
    cra_bin         = fields.Char(related='partner_id.cra_bin')
    link_email = fields.Char(related='alias_id.alias_name')


    # VARIOUS WORK PROCESSING STATUS #
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
    
    task_count            = fields.Integer(compute='_get_task_count')    

    ###################################
    # TRACK CLAIM ORGANIZATION FIELDS #
    ###################################
    folder_group            = fields.Many2one('sred_system.folder_groups', string='relation to folder group',
                                              ondelete='set null', required=True)
    folder                  = fields.Many2one('sred_system.work_folders',
                                  string="assigned folder",
                                  ondelete='cascade',
                                  track_visibility='on_change', required=True)

    claim_type               = fields.Many2one('sred_system.claim_types',
                                  string='claim type',
                                  ondelete='set null',
                                  track_visibility='on_change')

    tax_years               = fields.Many2many('sred_system.tax_years','taxyear_id','tax_years', required=True)
    
    ####################
    # FINANCIAL FIELDS #
    ####################

    # Read only computed copies of the Estimated values
    # glitch in setting fields that requiring updating using views that are read-only turn fields into non-updatable
    # use the calculated fields instead on view forms to avoid the crazy glitch
    refund                  = fields.Float(compute='_calc_refund')
    fee                     = fields.Float(compute='_calc_fee')

    estimated_refund        = fields.Float()

    estimated_fee           = fields.Float()

    estimations             = fields.One2many('sred_system.work_estimations', 'estimate_id', string='Estimates')

    doc_count               = fields.Integer(compute='_get_attached_docs', string="Number of documents attached")
    
    manifest                = fields.Many2one('sred_system.manifest', string='manifest')



    ###############################
    # ROLES AND LEADERSHIP FIELDS #
    ###############################
    work_roles              = fields.One2many('sred_system.work_roles', 'work_role_id',
                                   string='assignment of work roles', ondelete='cascade')
    ####################
    # ALL OTHER FIELDS #
    ####################
    notes = fields.Html('Notes')

    all_emails = fields.One2many(related='task_ids.message_ids')

    emails = fields.One2many('sred_system.emails', 'claim_project')



    @api.model
    def make_alias(self):
        new_record = {}
        model1_tasks    = self.env['ir.model'].search([('model','=','sred_system.emails')]).id
        model2_parent   = self.env['ir.model'].search([('model','=','sred_system.claim_project')]).id
        new_record['alias_name'] = 'g'+str(randint(0, 999)) + '-' + str(self.search_count([('active','=',True)]))

        alias_defaults = {}
        new_record['alias_defaults'] = {'claim_project': self.id}
        new_record['alias_contact'] = 'everyone'
        new_record['alias_model_id'] = model1_tasks
        new_record['alias_parent_model_id'] = model2_parent
        new_record['alias_parent_thread_id'] = self.id
        new_alias = self.env['mail.alias'].create(new_record)
        self.alias_id = new_alias
        return


    @api.one
    def _get_task_count(self):
        this_obj = self.env['project.task'].search([('res_model','=','sred_system.claim_project'),('res_id','=',self.id)])
        if this_obj:
            self.task_count = len(this_obj)
        return
    
    
    @api.one
    def link_button_pressed(self):
        res = {}
        if self.id:
            if not self.alias_id:
                self.make_alias()
        return res


    @api.one
    @api.model
    def _calc_alias(self):
        if self.alias_id:
            self.email_feed = self.alias_id.display_name
        else:
            self.email_feed = "not set"
        return


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


    @api.model
    #  [('s1', 'Work'), ('s2','Greenlight'), ('s3', 'CRA'), ('s4', 'Claim-State')
    def _get_default_status(self, stage_id):
        _logger.debug('get default status ' + stage_id)
        new_record = []
        new_list = self.env['sred_system.processing_status'].search([('stage', '=', stage_id), ('is_default', '=', True)])
        if new_list:
            new_record = new_list[0]
        return new_record


    @api.model
    def _get_work_processing_status_default(self):
        return self._get_default_status('s1')

    @api.model
    def _get_glip_processing_status_default(self):
        return self._get_default_status('s2')

    @api.model
    def _get_cra_processing_status_default(self):
        return self._get_default_status('s3')

    @api.model
    def _get_claim_status_default(self):
        return self._get_default_status('s4')


    @api.model
    def _get_current_estimate(self):
        _logger.debug('calculating current estimate (START)')
        answer = []
        fee_amount = 0.00
        refund_amount = 0.00
        found_one = False
        if self.estimations:
            for my_rec in self.estimations:
                _logger.debug('......')
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
        _logger.debug('calculating current estimate (END)')
        return answer


    @api.one
    @api.onchange('estimations')
    def calc_estimation_on_claim(self):
        _logger.debug('estimations changed')
        response = self._get_current_estimate()
        self.estimated_fee = response[0]
        self.estimated_refund = response[1]
        self._calc_fee
        self._calc_refund
        _logger.debug('estimates changed end')
        return True


    @api.one
    @api.model
    def _get_attached_docs(self):
        attachments = self.env['ir.attachment'].search([('res_model', '=', 'sred_system.claim_project'), ('res_id', '=', self.id)])
        if attachments:
            self.doc_count = len(attachments)
        else:
            self.doc_count = 0
        return len(attachments) or 0


    def open_website_action(self, cr, uid, id, default=None, context=None):
        rec = self.browse(cr, uid, id, context=context)
        this_web = rec.website
        if this_web:
            response = {
                 'type'     : 'ir.actions.act_url',
                 'target'   : 'new',
                 'url'      : this_web
                       }
        return response



    def attachment_tree_view(self, cr, uid, ids, context):
        domain = [('res_model', '=', 'sred_system.claim_project'), ('res_id', 'in', ids)]
        res_id = ids and ids[0] or False
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Documents are attached to the claim files.</p><p>
                        Send messages or log internal notes with attachments to link
                        documents to your project.
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, res_id)
        }


    
    def manifest_button_pressed(self, cr, uid, id, context):
        rec = self.browse(cr, uid, id, context=context)
        this_domain = [('res_model','=',self._name),('res_id','=',rec.id)]
        response = {
            'name': _('Manifest'),
            'domain': this_domain,
            'res_model': 'sred_system.manifest',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Each claim may have a single manifest to add role specific documents into.</p><p>
                        </p>'''),
            }
        return response
        
        
    @api.multi                                   
    def open_tasks(self):
        this_id         = self.ids
        this_record     = self.env['sred_system.claim_project'].browse(this_id)
        context         = {}
        response        = {}
        domain          = []
     
        context['default_res_model']    = 'sred_system.claim_project'
        context['default_single_task_mode'] = True
        
        response['name']                = _('Tasks')
        response['res_model']           = 'project.task'
        response['type']                = 'ir.actions.act_window'
        response['view_id']             = False
        response['view_mode']           = 'kanban,tree,calendar,form'
        response['view_type']           = 'form'
        response['help']                = _('Tasks assigned to claim may also appear under customer')
        response['limit']               = 80
        
        if this_record:
  
            if this_record.partner_id:
                context['default_partner_id'] = this_record.partner_id.id
 
            domain                    = [('res_id','=', this_record.id), ('res_model','=', 'sred_system.claim_project')]
            context['default_res_id'] = this_record.id
 
        response['domain'] = domain
        response['context'] = context
        print response
        
        return response   
    
    
    
    
    
    
     
        
    def calendar_button_pressed(self, cr, uid, ids, context):
        return {
            'name': 'Meetings',
            'res_model': 'calendar.event',
            'type':'ir.actions.act_window',
            'view_id':False,
            'view_mode':'calendar,tree,form',
            'view_type':'Calendar'}

    
    def email_button_pressed(self, cr, uid, ids, context):
        return {
                'name': 'Email',
                'res_model': 'mail.mail',
                'type':'ir.actions.act_window',
                'view_id':'view_mail_form',
                'view_mode':'form',
                'view_type':'form'}

    # When the partner id changes, change the list of contracts also.  Contracts are associates with only specific partners
    @api.onchange('partner_id')
    def on_change_work_scope(self):
        res = {}
        filter = {}
        filter['contracted_service'] = [('partner_id', '=', self.partner_id.id)]
        res['domain'] = filter
        return res




    _order = "sequence, name, id"
    _defaults = {
        'active': True,
        'sequence': 10,
        'user_id': lambda self,cr,uid,ctx: uid,
        'name': "New Claim",
        'tax_years': _get_tax_year_defaults,
        'claim_type': _get_default_claim_type,
        'claim_status': _get_claim_status_default,
        'work_processing_status': _get_work_processing_status_default,
        'glip_processing_status': _get_glip_processing_status_default,
        'cra_processing_status': _get_cra_processing_status_default}



