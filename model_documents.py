from openerp import models, fields, api
import time
import logging
from openerp.tools.translate import _

_logger = logging.getLogger('sred_system.documents')


class my_modifications_to_documents(models.Model):
    _inherit = 'ir.attachment'
     
#     tasks = fields.One2many('project.task', 'id', string='Task Assigned')
    use_tasks   = fields.Boolean(default=False)
    track_sred  = fields.Boolean(default=False)
                           
    request_notes = fields.Html()
    
    
    
#    [('_info_request_existing','Existing'),('_info_request_new','New')]
#    _selection_sources_request_is_new      = [('_info_internal_form','Form'),('_info_google_drive','Google Drive'),('_info_survey','Survey/Ask')]
#    _selection_sources_request_is_existing = [('_info_upload','Upload'),('_info_internal_form','Form'),('_info_google_drive','Google Drive')]
    

     
     
     
     
     
    
