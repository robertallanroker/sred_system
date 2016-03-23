from openerp import models, fields, api, osv
import logging
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

    # Its silly that there is no field for website in a lead.  Opportunities contain website
    # information in their assigned partners but leads haven't been converted nor contain a partner record.
    web_url = fields.Char()
    # This would be useful to display related website data onto the primary form.
    # website = fields.Char(related="res.partner.website")

    more_contacts = fields.Many2many('res.partner', 'crm_id','more_contacts', string='contacts')
    
    crm_group = fields.Many2one('sred_system.crm_groups', string='Selling Group')
    selling_group = fields.Char(related='crm_group.name')
    
    claim_file = fields.Many2one('sred_system.claim_project', string='assigned claim file')

    #  target_profile = fields.One2Many('sred_system.crm_targeting', 'targets', "targeting_profile_dna")

    @api.model
    @api.onchange("crm_group")
    def _on_crm_group_changes(self):
        if self.crm_group:
            self.color = self.crm_group.color
  
    def _invoke_new_window(self, new_url):
        resp = {}
        if new_url:
            resp = {
                  'type'     : 'ir.actions.act_url',
                  'target'   : 'new',
                  'url'      : new_url
               }
        return resp

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