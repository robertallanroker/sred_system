from openerp import models, fields, api, osv
import logging
import datetime
from openerp.tools.translate import _

class my_changes_to_projects(models.Model):
    _inherit = 'project.project'
    
    track_sred = fields.Boolean()
    
class my_changes_to_tasks(models.Model):
    _inherit = ['project.task']
    
    project_track_sred = fields.Boolean(related='project_id.track_sred')
    track_sred = fields.Boolean()
    
    res_model = fields.Char()
    res_id = fields.Integer()
    
    document_count = fields.Integer(compute="_count_documents")
    project_display_name = fields.Char(related='project_id.display_name')
    project_partner_id = fields.Many2one(related='project_id.partner_id')
    single_task_mode = fields.Boolean()
    
    delegate_to = fields.Many2one('res.partner', string='Delegate to', domain = "[('res_group.name','=','Contact')]")
    
    completed = fields.Boolean(default=False)
    completed_on = fields.Datetime()
    
    due_this_week = fields.Boolean(compute="_calc_due_dates")
    due_this_month = fields.Boolean()
    due_overdue    = fields.Boolean()

    @api.model
    def get_date_year(self, this_date):
        return getattr(this_date,'year')
    
    @api.model
    def get_date_month(self, this_date):
        return getattr(this_date,'month')
    
    @api.model
    def get_date_day(self, this_date):
        return getattr(this_date,'day')
    
    @api.model
    def is_this_week(self, this_date):
        this_today = datetime.datetime.now().strftime('%m-%d-%Y') 
        this_day = self.get_date_day(this_today)
        this_val = self.get_date_day(this_date)
        return this_val == this_day
    
    @api.model
    def is_this_month(self, this_date):
        this_today = datetime.datetime.now().strftime('%m-%d-%Y') 
        this_month = self.get_date_month(this_today)
        this_val   = self.get_date_month(this_date)
        return this_month == this_val
    
    @api.model
    def is_this_year(self, this_date):
        this_today = datetime.datetime.now().strftime('%m-%d-%Y')
        this_year = self.get_date_year(this_date)
        this_val  = self.get_date_year(this_today)
        return this_year == this_val
    
    
    @api.one
    def _calc_due_dates(self):
        this_due_overdue = False
        this_due_this_week = False
        this_due_this_month = False
        if not self.completed:
            if self.date_deadline:
                if self.date_deadline < datetime.datetime.now().strftime('%m-%d-%Y'):
                    this_due_overdue = True
                else:
                    if self.is_this_year(self.date_deadline):
                        this_due_this_month = self.is_this_month(self.date_deadline)
                        this_due_this_week = self.is_this_week(self.date_deadline)
        self.due_this_week = this_due_this_week
        self.due_this_month = this_due_this_month
        self.due_overdur = this_due_overdue
        return
            
    @api.one
    def _count_documents(self):
        if self.attachment_ids:
            self.document_count = len(self.attachment_ids)
        else:
            self.document_count = 0
        return
    
    
    @api.multi
    def get_current_record(self):
        this_id         = self.ids
        this_record     = self.env[self._name].browse(this_id)
        return this_record
    
    
    @api.one
    @api.onchange('single_task_mode')
    def _on_single_task_mode_changed(self):
        if self.single_task_mode:
            self.project_id = False
        return  
    
            
    @api.one
    @api.onchange('project_id')
    def _on_prohject_id_changed(self):
        if self.project_id != False:
            self.single_task_mode = True
        return
    
    
    @api.multi
    def toggle_completed(self):
        this_id = self.ids
        this_record = self.env['project.task'].browse(this_id)
        if this_record:
            self.completed = not self.completed
        if this_record.completed:
            self.completed_on = fields.Date.today()
        return
    
            
    @api.multi                                   
    def open_documents(self):
        this_id = self.ids
        this_record = self.env['project.task'].browse(this_id)
        context = {}
        response = {}
        domain = []
     
        context['default_res_model'] = 'project.task'
        context['default_res_name'] = 'Tasks'
        
        response['name'] = _('Documents')
        response['res_model'] = 'ir.attachment'
        response['type'] = 'ir.actions.act_window'
        response['view_id'] = False
        response['view_mode'] = 'kanban,tree,form'
        response['view_type'] = 'form'
        response['help'] = _('Upload Documents. Tasks assigned to users and customers, will also be linked together')
        response['limit'] = 80
        
        if this_record:
  
            if this_record.partner_id:
                context['default_partner_id'] = this_record.partner_id.id
 
            domain = [('res_id', '=', this_record.id), ('res_model', '=', 'project.task')]
            context['default_res_id'] = this_record.id
 
        response['domain'] = domain
        response['context'] = context
        
        
        
        return response

    # All new records should be opt-out by 
