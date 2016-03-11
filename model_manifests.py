from openerp import models, fields, api


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
    res_model = fields.Integer()
    res_id    = fields.Integer()
    
    # The list of documents that are organized with each manifest
    information = fields.One2many('sred_system.manifest_information','manifest', string='Information')
    description = fields.Html()
    
    # For convenience we can track the count of documents
    information_count = fields.Integer(compute='_get_information_count')
    
    @api.model
    def _get_information_count(self):
        if self.docs:
            self.information_count = len(self.docs)
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
    
    
    
# Information is in either the following forms:
#   1. New
#        Someone needs to supply the details 
#   2. Existing
#        Some needs to supply existing information
class my_reference_to_information(models.Model):
    _name = "sred_system.manifest_info_reference"
    
    _selection_request = [('_info_request_new','New'),('_info_request_existing','Existing')]
    _selection_sources = [('_info_upload','upload'),('_info_internal_form','form'),('_info_google_drive','google'),('_info_survey','survey/ask')]
    source  = fields.Selection(selection=_selection_sources)
    request = fields.Selection(selection=_selection_request)
        
    # Attachment
    request_attachment = fields.Many2one('ir.attachment', 'Request Template')
    
    # Something found by locating it in another model
    # We can create a new record if needed
    # To-do: figure out how to use this to push out a specific survey
    res_model   = fields.Char()
    res_id      = fields.Integer()
    



# sred_system.manifest_docs
# Documents are organized and encapsulated to provide added functionality.
class my_manifest_information(models.Model):
    _name = 'sred_system.manifest_information'
    _description = 'Encapsulate documents with new functionality within a Manifest'
    _inherit     = 'sred_system.manifest_info_reference'
      
    name            = fields.Char(string='Documentation Label')
    manifest        = fields.Many2one('sred_system.manifest', string='Information Manifest')
    info_type       = fields.Many2one('sred_system.manifest_info_types', string='Information Type')
    info_format     = fields.Many2one('sred_system.manifest_info_formats', string='Information Format')
    description     = fields.Html()
    
    # For convenience we can pull the related scope, since its based the currently selected 
    # manifest type
    scope   = fields.Many2one('sred_system.manifest', string='scope')
    
    # We can assign a single task if we like, if needed to get requested information
    task            = fields.Many2one('sred_system.sred_project_tasks', string='Task')

    


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
    scope   = fields.Many2one('sred_system.manifest', string='scope')    ## To determine what types are available to what scope areas

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
    
 
    
    
    
    
        
    
    
    
    
    
    
       
    
    
    
    