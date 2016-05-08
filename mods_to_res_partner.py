from openerp import models, fields, api, osv
from openerp.tools.translate import _

# New relationship to support groups of res.partners
class my_res_partner_groups(models.Model):
    _name = "sred_system.res_partner_groups"
    sequence = fields.Integer()
    name     = fields.Char()
    is_default = fields.Boolean()
    is_company = fields.Boolean()
    is_customer= fields.Boolean()
    is_vendor  = fields.Boolean()
    partner_id = fields.One2many('res.partner','res_group','partner')
         
    _defaults  = {'is_company': True, 'is_customer': True, 'is_vendor': True}
    
# res.partner changes
class my_changes_to_customers(models.Model):

    _inherit = 'res.partner'

    # These additional fields are specific format fields for Revenue Canada and Business Accounts
    cra_bin = fields.Char()             # Canada Revenue Agency Business Information Number
    cra_year_end = fields.Datetime()    # Canada Revenue Agency Financial Year End

    # We do not like the various boolean status's that have limited grouping functionality
    # i.e is_customer, is_vendor, etc... We use a group status relationship so we can group account properly
    # unfortunately we have to add backwards defaults to support the old-style boolean flags so we don't break other 
    # parts of the system
    res_group = fields.Many2one('sred_system.res_partner_groups','group')
    res_group_name = fields.Char(related='res_group.name')
    
    # Would like to see all the SRED claims processed for a particular partner 
                                
    # There should be a list of user types
    user_sales   = fields.Many2one('res.users', string = 'sales person')
    user_account = fields.Many2one('res.users', string = 'account manager')
    user_leadgen = fields.Many2one('res.users', string = 'lead generated')
    
    contracts_count = fields.Integer(compute='_get_contracts_count')
    claims_count    = fields.Integer(compute='_get_claims_count')
    
    res_model       = fields.Char(default='res.partner')
    res_id          = fields.Integer(default=0)

    @api.one
    @api.model
    def _get_contracts_count(self):
        contracts_obj = self.env['sred_system.sred_contracts'].search([('partner_id','=',self.id)])
        if contracts_obj:
            self.contracts_count = len(contracts_obj)
        else:
            self.contracts_count = 0
        return
    
    @api.one
    @api.model
    def _get_claims_count(self):
        claims_obj = self.env['sred_system.claim_project'].search([('partner_id','=',self.id)])
        if claims_obj:
            self.claims_count = len(claims_obj)
        else:
            self.claims_count = 0
        return
    
    
    @api.model
    @api.onchange('res_group')
    def group_has_changed(self):
        if self.res_group:
            self.customer = self.res_group.is_customer
            self.supplier = self.res_group.is_vendor
            self.is_company = self.res_group.is_company
            if self.is_company:
                self.company_type = 'company'
            else:
                self.company_type = 'person'

            
        return
    
    
    @api.model
    @api.onchange('user_id')
    def on_changed_sales_person(self):
        if self.user_id:
            if not self.account_manager:
                self.account_manager = self.user_id
        return    
    
    
    @api.model
    def _get_default_group(self):
        newrecord=[]
        this_rec = self.env['sred_system.res_partner_groups'].search([('is_default','=',True)])
        if this_rec:
            newrecord = this_rec[0]
        return newrecord 


                
    def open_claims(self, cr, uid, id, context):
        domain = [('partner_id','=',id)]
        return {
            'name': _('Claims'),
            'domain': domain,
            'res_model': 'sred_system.claim_project',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Documents are attached to the claim files.</p><p>
                        Send messages or log internal notes with attachments to link
                        documents to your project.
                    </p>'''),
            'limit': 80,
            'context': "{'default_partner_id': %d}" %id[0]
        }


    
    def open_contracts(self, cr, uid, id, context):
        domain = [('partner_id','=',id)]
        return {
            'name': _('Contracts'),
            'domain': domain,
            'res_model': 'sred_system.sred_contracts',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Documents are attached to the claim files.</p><p>
                        Send messages or log internal notes with attachments to link
                        documents to your project.
                    </p>'''),
            'limit': 80,
            'context': "{'default_partner_id': %d}" %id[0]
        }


    
    # ODOO makes all new res partner's a customer by default.  Res_partner is being used in large marketing lists
    # and opportunities.  The assignment of a customer flag makes thousands of incorrect status
    _defaults = {'is_customer': False, 'res_group': _get_default_group}
    
    
    

    