from openerp import models, fields, api, osv
import logging
from openerp.tools.translate import _

_logger = logging.getLogger('sred_system')


class my_crm_groups(models.Model):
    _name = 'sred_system.crm_groups'
    
    name = fields.Char()
    color = fields.Integer()
    
    crm_records = fields.One2many('crm.lead','id', string='crm records')
    
    _defaults={'color':0}
    

class my_changes_to_crm_leads(models.Model):
    _inherit = 'crm.lead'

    # All new records should be opt-out by default per regulatory conditions today
    opt_out = fields.Boolean(default=True)

    is_customer_opportunity = fields.Boolean(default=False)
    
    # Its silly that there is no field for website in a lead.  Opportunities contain website
    # information in their assigned partners but leads haven't been converted nor contain a partner record.
    web_url = fields.Char()
    # This would be useful to display related website data onto the primary form.
    # website = fields.Char(related="res.partner.website")
   
    crm_group = fields.Many2one('sred_system.crm_groups', string='Selling Group')
    selling_group = fields.Char(related='crm_group.name')
    
    claim_file = fields.Many2one('sred_system.claim_project', string='assigned claim file')
       
    task_count = fields.Integer(compute="_calc_task_count")
    contact_count = fields.Integer(compute="_calc_contact_count")
    
    partner_id = fields.Many2one('res.partner', domain=[('is_company','!=',False),('customer','!=',False)], string="Customer" ) 
    
    other_partner_id = fields.Many2one('res.partner', string='Other Account', domain=[('is_company','!=',False),('customer','=',False)] )

    #  target_profile = fields.One2Many('sred_system.crm_targeting', 'targets', "targeting_profile_dna")


    @api.model
    @api.onchange("crm_group")
    def _on_crm_group_changes(self):
        if self.crm_group:
            self.color = self.crm_group.color
  
    @api.one
    @api.onchange("is_customer_opportunity")
    def _on_cust_opp_changed(self):
        if self.is_customer_opportunity:
            self.other_partner_id = False
        else:
            self.partner_id = False
        return
        
      
    def _invoke_new_window(self, new_url):
        resp = {}
        if new_url:
            resp = {
                  'type'     : 'ir.actions.act_url',
                  'target'   : 'new',
                  'url'      : new_url
               }
        return resp
    
    
    @api.one
    def _calc_task_count(self):
        this_domain = [('res_model','=',self._name),('res_id','=',self.id)]
        this_object = self.env['project.task'].search(this_domain)
        if this_object:
            self.task_count = len(this_object)
        else:
            self.task_count = 0
        return
    
    
    @api.one
    def _calc_contact_count (self):
        
        this_partner_id = False
        this_domain     = []
        
        if self.is_customer_opportunity:
            this_partner_id = self.partner_id.id
        else:
            this_partner_id = self.other_partner_id.id
            
        if this_partner_id:
            this_domain = [
                      '|', 
                      '&', ('id','=',this_partner_id),('company_type','=','Individual'),
                      '&', ('res_model', '=', 'crm.lead'), ('res_id', '=', self.id)
                     ]
        else:
            this_domain = [('res_model', '=', 'crm.lead'), ('res_id', '=', self.id), ('company_type','=','Individual')]
            
        this_object = self.env['res.partner'].search(this_domain)
        
        if this_object:
            self.contact_count = len(this_object)
        else:
            self.contact_count = 0
        
        return


    def _clean_parameter(self, param):
        p = ''
        if param:
            p = param
        return p


    def _join_search(self, url1, url2, joinchar):
        join_new_url = ''
        if url1 and (len(url1) > 0):
            join_new_url = url1 + joinchar + url2
        else:
            join_new_url = url2
        return join_new_url


    def _fix_web_http(self, url):
        new_url = url
        if not 'www.' in new_url:
            new_url = 'www.'+new_url
        if not 'http://' in new_url:
            new_url = 'http://' + new_url
        return new_url


    def perform_open_website(self, cr, uid, id, default=None, context=None):
        rec = self.browse(cr, uid, id, context=context)

        if rec.web_url:
            this_web = rec.web_url
        else:
            this_web = 'google.com'

        return self._invoke_new_window(self._fix_web_http(this_web))
   
   
    @api.multi                                   
    def open_tasks(self):
        this_id         = self.ids
        this_record     = self.env['crm.lead'].browse(this_id)
        context         = {}
        domain           = []
        this_partner_id = this_id
        
        if this_record:
            
            this_partner_id = self._get_correct_partner_id(this_record) 

            if this_partner_id:
                domain  = ('res_model', '=', 'crm.lead'), ('res_id', '=', this_record.id)
                context = {'default_res_model':'crm.lead','default_res_id': this_record.id, 'default_partner_id': this_partner_id}
            else:
                domain  = ('res_model', '=', 'crm.lead'), ('res_id', '=', this_record.id)
                context = {'default_res_model':'crm.lead','default_res_id': this_record.id}

        return {        
             'name': _('Opportunity Tasks'),
            'domain': domain,
            'res_model': 'project.task',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',         
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Assign contacts to the lead.  Customer contacts when selected appear automatically.
                    </p>'''),
            'limit': 80,
            'context': context,
        }

        
                
            
    @api.one
    def _get_correct_partner_id(self, this_record):
        this_partner_id = False
        
        if this_record:        
            if this_record.is_customer_opportunity:
                this_partner_id = this_record.partner_id.id
            else:
                this_partner_id = this_record.other_partner_id.id
        
        return this_partner_id
    
         
    @api.multi
    def open_contacts(self):
        this_id     = self.id
        this_record = self.env['crm.lead'].browse(this_id)
        context     = {}
        domain      = []
        this_partner_id = this_id
        
        if this_record:
            
            this_partner_id = self._get_correct_partner_id(this_record)
    
            if this_partner_id:
                domain = [
                          '|', 
                          '&', ('id','=',this_partner_id),('company_type','=','Individual'),
                          '&', ('res_model', '=', 'crm.lead'), ('res_id', '=', this_id)
                         ]
                context = {
                       'default_res_model': 'crm.lead',
                       'default_res_id': this_id,
                       'default_company_type': 'Individual',
                       'default_company_id' : this_partner_id,
                       'default_supplier' : False,
                       'default_street': this_record.street,
                       'default_city': this_record.city,
                       'default_zip': this_record.zip,
                       }
            else:
                domain = [('res_model', '=', 'crm.lead'), ('res_id', '=', this_id), ('company_type','=','Individual')]
                context = {
                       'default_res_model': 'crm.lead',
                       'default_res_id': this_id,
                       'default_company_type': 'Individual',
                       'default_supplier': False,
                       'default_street': this_record.street,
                       'default_city': this_record.city,
                       'default_zip': this_record.zip,
                       }
            
            return {
            'name': _('Contacts'),
            'domain': domain,
            'res_model': 'res.partner',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban, tree,form',         
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Assign contacts to the lead.  Customer contacts when selected appear automatically.
                    </p>'''),
            'limit': 80,
            'context': context,
        }


    #http://www.manta.com/search?search_source=nav&pt=49.17%2C-123.136795&search_location=Richmond+BC&search=accent+steal
    def perform_manta_search(self, cr, uid, id, default=None, context=None):
        rec = self.browse(cr, uid, id, context=context)
        this_web = self._join_search('https://www.google.ca?gws_rd=ssl#q=',self._clean_parameter(rec.partner_name) ,'+')
        this_web = self._join_search(this_web,'MANTA',' ')
        return self._invoke_new_window(this_web)

 
    def perform_google_search(self, cr, uid, id, default=None, context=None):
        rec = self.browse(cr, uid, id, context=context)
        this_web = self._clean_parameter(rec.partner_name)
        # https://www.google.ca/search?q=google+search+bar
        #https://www.google.ca/?gws_rd=ssl#q=accent+steal
        this_invoke = 'https://www.google.ca?gws_rd=ssl#q=' + this_web
        return self._invoke_new_window(this_invoke)

    def perform_linkedin_search(self, cr, uid, id, default=None, context=None):
        rec = self.browse(cr, uid, id, context=context)
        this_web = rec.partner_name
        this_invoke = 'http://www.linkedin.com/vsearch/f?type=all&keywords=' + rec.partner_name
        # http://www.manta.com/search?search_source=nav&pt=49.17%2C-123.136795&search_location=Richmond+BC&search=green
        return self._invoke_new_window(this_invoke)

    #https://www.facebook.com/public?query=wwww&type=people
    def perform_facebook_person_search(self, cr, uid, id, default=None, context=None):
        rec = self.browse(cr, uid, id, context=context)
        this_web = self._clean_parameter(rec.contact_name)
        this_invoke = 'https://www.facebook.com/public?query='
        if rec and len(this_web) > 0:
            this_invoke = self._join_search(this_invoke, this_web,'')
            this_invoke = self._join_search(this_invoke, 'type=people','&')
        return self._invoke_new_window(this_invoke)

    def perform_facebook_business_search(self, cr, uid, id, default=None, context=None):
        rec = self.browse(cr, uid, id, context=context)
        this_web = self._clean_parameter(rec.partner_name)
        this_invoke = 'https://www.facebook.com/public?query='
        if rec and len(this_web) > 0:
            this_invoke = self._join_search(this_invoke, this_web,'')
            this_invoke = self._join_search(this_invoke, 'type=pages&init=dir&nomc=0','&')
        return self._invoke_new_window(this_invoke)


    # https://www.facebook.com/public?query=robert+roker&type=people
    # https://www.facebook.com/public?query=greenlightip&type=pages&init=dir&nomc=0