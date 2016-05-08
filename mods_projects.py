from openerp import models, fields, api, osv
import logging
from openerp.tools.translate import _

class my_changes_to_projects(models.Model):
    _inherit = 'project.project'
    
    track_sred = fields.Boolean()
    
class my_changes_to_tasks(models.Model):
    _inherit = 'project.task'
    
    project_track_sred  = fields.Boolean(related='project_id.track_sred')
    track_sred          = fields.Boolean()
    
    res_model           = fields.Char()
    res_id              = fields.Integer()
    
    document_count       = fields.Integer(compute="_count_documents")
    project_display_name = fields.Char(related='project_id.display_name')
    project_partner_id   = fields.Many2one(related='project_id.partner_id')
    single_task_mode     = fields.Boolean()
    
    delegate_to          = fields.Many2one('res.partner', string='Delegate to')
    
    completed            = fields.Boolean(default=False)

    
    @api.one
    def _count_documents(self):
        if self.attachment_ids:
            self.document_count = len(self.attachment_ids)
        else:
            self.document_count = 0
        return
    
    
    @api.one
    @api.onchange('single_task_mode')
    def _on_single_task_mode_changed(self):
        if self.single_task_mode:
            self.project_id = False
        return
            
            
    @api.multi                                   
    def open_documents(self):
        this_id         = self.ids
        this_record     = self.env['project.task'].browse(this_id)
        context         = {}
        response        = {}
        domain          = []
     
        context['default_res_model']    = 'project.task'
        context['default_res_name']     = 'Tasks'
        
        
        response['name']                = _('Documents')
        response['res_model']           = 'ir.attachment'
        response['type']                = 'ir.actions.act_window'
        response['view_id']             = False
        response['view_mode']           = 'kanban,tree,form'
        response['view_type']           = 'form'
        response['help']                = _('Upload Documents. Tasks assigned to users and customers, will also be linked together')
        response['limit']               = 80
        
        if this_record:
  
            if this_record.partner_id:
                context['default_partner_id'] = this_record.partner_id.id
 
            domain                    = [('res_id','=', this_record.id), ('res_model','=', 'project.task')]
            context['default_res_id'] = this_record.id
 
        response['domain'] = domain
        response['context'] = context
        
        
        
        return response

    # All new records should be opt-out by 