from openerp import models, fields, api
import time
import logging

_logger = logging.getLogger('sred_system.manifest')


class my_document_manifest(models.Model):
    _name = 'sred_system.manifest'
    _description = 'Organize documents related to work breakdown'
    name  = fields.Char()
    
    # There are scope area's (GLIP, CRA, CUSTOMER) that define groups of documents
    # by who is responsible for them.  The only purpose of this field
    # is for user display purposes.
    user_scope_switch = fields.Many2one('sred_system.work_scope', string='scope', ondelete='cascade')
    
    # Manifests can be used for any model we assign to it or there may be multiple models that 
    # reference it.
    res_model = fields.Many2one('ir.model', string='belongs to model')
    res_id    = fields.Integer(string='associated to model id')
    
    # The list of documents that are organized with each manifest
    information = fields.One2many('sred_system.manifest_information','manifest', string='Information')
    description = fields.Html()
    
    # For convenience we can track the count of documents
    information_count = fields.Integer(compute='_get_information_count')
    
    @api.model
    def _get_information_count(self):
        if self.information:
            self.information_count = len(self.information)
        else:
            self.information_count = 0
        return 
    
    @api.onchange('user_scope_switch')
    def _on_user_scope_switched(self):
        afilter = {}
        res     = {}
        afilter['information'] = [('scope.id','=',self.user_scope_switch.id)]
        res['domain'] = afilter
        return res
            
    @api.model
    @api.onchange('information')
    def _on_doc_changes(self):
        self._get_information_count
        return
    
    
    # Convenience s/r, used to assign the currently referenced record
    # to a specific model and id.   
    @api.one
    def assign_model(self, this_model, this_model_id):
        self.res_model = this_model
        self.res_id    = this_model_id
    
    
    _defaults = {'user_scope_switch':1}
    
# Information is in either the following forms:
#   1. New
#        Someone needs to supply the details 
#   2. Existing
#        Some needs to supply existing information
class my_reference_to_information(models.Model):
    _name = "sred_system.manifest_info_reference"
    
    version = fields.Float(compute="_compute_version")
    version_major = fields.Integer()
    version_minor = fields.Integer()

    _selection_request                     = [('_info_request_existing','Existing'),('_info_request_new','New')]
    _selection_sources_request_is_new      = [('_info_internal_form','Form'),('_info_google_drive','Google Drive'),('_info_survey','Survey/Ask')]
    _selection_sources_request_is_existing = [('_info_upload','Upload'),('_info_internal_form','Form'),('_info_google_drive','Google Drive')]
    _selection_sources_current             = _selection_sources_request_is_existing
     
    source  = fields.Selection(selection=_selection_sources_current)
    request = fields.Selection(selection=_selection_request)
        
    # Attachment
    request_attachment      = fields.Many2one('ir.attachment', 'Attachment')
    request_url_reference   = fields.Char()
    request_gdrive_template = fields.Many2one('google.drive.config', string='Google Drive Template')
    request_survey          = fields.Char()
    
    # Something found by locating it in another model
    # We can create a new record if needed
    # To-do: figure out how to use this to push out a specific survey
    res_model   = fields.Many2one('ir.model', string='model')
    res_id      = fields.Integer()
    
    who_requested = fields.Many2one('res.users', 'assigned person', ondelete='set null')
    who_date      = fields.Datetime()
    format_wholine_in_tree = fields.Char(compute='_compute_who')
     
    @api.one
    def assign_to(self, this_model, this_id):
        if this_model:
            self.res_model = this_model
            self.res_id    = this_id
        return
    
    @api.one
    def _assign_sources(self):
        if 'info_request_new' in self._selection_request:
            self._selection_sources_current = self._selection_sources_request_is_new
        else:
            self._selection_sources_current = self._selection_sources_request_is_existing
        return self._selection_souces_current
    
    @api.onchange('request')
    def _on_request_has_changed(self):
        self._assign_sources
        return
  
    @api.model
    def _get_default_request(self):
        # self.request = '_info_request_existing'
        return
    
    @api.one
    def _inc_major(self):
        self.version_major = self.version_major + 1
        return
    
    @api.one
    def _inc_minor(self):
        self.version_minor = self.version_minor + 1
        return
    
    @api.model
    def _compute_version(self):
        self.version = (self.version_major) + (self.version_minor / 10)
        return self.version
    
    @api.one
    def _compute_who(self):
        fline=''
        if self.who_date:
            fline = self.who_date
        else:
            fline = ''
        if self.who_requested:
            fline = self.who_requested.name + ', ' + fline
        else:
            fline = '(unknown), ' + fline
        _logger.info(fline)   
        self.format_wholine_in_tree = fline
        return fline
    
    _defaults = {'request':_get_default_request, 
                 'who_requested': lambda self,cr,uid,ctx: uid,
                 'who_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
                 'version_major':1,
                 'version_minor':0
                 } 

# sred_system.manifest_docs
# Documents are organized and encapsulated to provide added functionality.
class my_manifest_information(models.Model):
    _name = 'sred_system.manifest_information'
    _description = 'Encapsulate documents with new functionality within a Manifest'
    _inherit    = 'sred_system.manifest_info_reference'
      
    name            = fields.Char(string='Documentation Label')
    manifest        = fields.Many2one('sred_system.manifest', string='Information Manifest')
    info_type       = fields.Many2one('sred_system.manifest_info_types', string='Information Type')
    info_format     = fields.Many2one('sred_system.manifest_info_formats', string='Information Format')
    description     = fields.Html()
    
    # For convenience we can pull the related scope, since its based the currently selected 
    # manifest type
    scope   = fields.Many2one('sred_system.work_scope', string='role area')
    
    # We can assign a single task if we like, if needed to get requested information
    task            = fields.Many2one('sred_system.sred_project_tasks', string='Task')

    date_deadline  = fields.Date(related='task.date_deadline')
    description    = fields.Html(related='task.description')
    assigned_to    = fields.Many2one(related='task.assigned_to')
    is_completed   = fields.Boolean(related='task.completed')
   
    @api.model
    def create(self, values):
        new_id = super(my_manifest_information, self).create(values)
        self._assign_task
        return new_id  
    
    @api.one    
    @api.onchange('scope')  
    def _on_scope_changed(self):
        this_filter = {}
        this_domain = {}
        this_filter['info_type'] = [('scope', '=', self.scope)]
        this_domain['domain'] = this_filter
        return this_domain
    
    @api.one
    def _assign_task(self):
        if not self.task:
            new_vals = {}
            new_vals['name'] = 'to do'
            new_task_obj = self.env('sred_system.sred_project_tasks').create(new_vals)
            self.task = new_task_obj.id
            _logger.info('new task created in manifest information document')
        return
    
    def button_pressed_open_task(self, cr, uid, id, default=None, context=None):
        self._assign_task
        rec = self.browse(cr, uid, id, context=context)
        response = {}
        if rec.task:
            this_task_id = rec.task.id
            response = {
            'name': _('Information Task'),
            'domain': [('id','=',this_task_id)],
            'res_model': 'sred_system.sred_project_tasks',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Each claim may have a single manifest to add role specific documents into.</p><p>
                        </p>'''),
            }
        else:
            _logger.info('no task to open')
        return response
    
    def button_pressed_completed_task(self, cr, uid, id, default=None, context=None):
        self._assign_task
        rec = self.browse(cr, uid, id, context=context)
        if rec:
            rec.completed = not rec.completed
        return
    
      
        

#  sred_system.manifest_types
#  Contains the logic behind what type of information is being recorded within the 
#  manifested documents
#  Request is:
#        Reference
#            to a Form
#            to a uploaded file
#            to a google drive location
#            to a push survey or questions
#        Template
#            to a google drive location only
#  Examples of types:
#    emails, Specifications, T2, RC59, Pictures, Videos, fax, notices, etc.
#    * predefined types are load_data
# THESE ARE MY TEMPLATES
class my_manifest_types(models.Model):
    _name        = 'sred_system.manifest_info_types'
    _description = 'Specify what type of information is referenced'
    _inherit     = 'sred_system.manifest_info_reference'
 
    # Info Reference inheritance is used to only contain the default values used in information
    
    name    = fields.Char(string='information type')
    scope   = fields.Many2one('sred_system.work_scope', string='belongs to role area')    ## To determine what types are available to what scope areas

    information = fields.One2many('sred_system.manifest_information','info_type', string='Documents')



# sred_system.manifest_format
# Information in the manifest can be defined by the format the reference or attachment 
# actually is.
class my_sred_information_formats(models.Model):
    _name = 'sred_system.manifest_info_formats'
    _description = 'specify the format of either the referenced information or the attachment file'
   
    _file_extensions = [('_ext_xls','xls'),('_ext_doc','doc'),('_ext_unknown','unknown')]
    
    name      = fields.Char(string='format type')
    manifest  = fields.One2many('sred_system.manifest_information','info_format', string='Manifest Information')
    
 
    
    
    
    
        
    
    
    
    
    
    
       
    
    
    
    