from openerp import models, fields, api, osv

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

    # Each Business Account may have one more SRED Services Contracted 
    service_contracts = fields.One2many('sred_system.sred_contracts', 'contracted_service', string='service_contracts')
    
    # We do not like the various boolean status's that have limited grouping functionality
    # i.e is_customer, is_vendor, etc... We use a group status relationship so we can group account properly
    # unfortunately we have to add backwards defaults to support the old-style boolean flags so we don't break other 
    # parts of the system
    res_group = fields.Many2one('sred_system.res_partner_groups','group')
    
    # Would like to see all the SRED claims processed for a particular partner 
    sred_claims = fields.One2many('sred_system.claim_project','partner_id', string='sred claims')
                                #  domain=lambda self:[('partner_id','=',self.id)])
                                
    # There should be both a sales person and an account manager, even if they are the same person 
    account_manager = fields.Many2one('res.users', string = 'Account Manager')
    
    # Link Contacts to CRM for leads
    crm_id = fields.Many2many('crm.lead', 'more_contacts', 'crm_id', 'leads from contact')
    
    crm_opportunities = fields.One2many('crm.lead','partner_id',string='opportunities')

    @api.model
    @api.onchange('res_group')
    def group_has_changed(self):
        if self.res_group:
            self.is_customer = self.res_group.is_customer
            self.is_vendor   = self.res_group.is_vendor
            self.is_company  = self.res_group.is_company
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
    
    # ODOO makes all new res partner's a customer by default.  Res_partner is being used in large marketing lists
    # and opportunities.  The assignment of a customer flag makes thousands of incorrect status
    _defaults = {'is_customer': False, 'res_group': _get_default_group}
    
    
    

    