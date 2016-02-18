from openerp import models, fields, api, osv


# THE CRM Module needs to be enhanced as follows
# Modifications to the existing structure
class my_changes_to_crm_leads_step1(models.Model):
    _inherit = 'crm.lead'

    # All new records should be opt-out by default per regulatory conditions today
    opt_out = fields.Boolean(default=True)

    # Its silly that there is no field for website in a lead.  Opportunities contain website
    # information in their assigned partners but leads haven't been converted nor contain a partner record.
    web_url = fields.Char()
    # This would be useful to display related website data onto the primary form.
    # website = fields.Char(related="res.partner.website")

 #  target_profile = fields.One2Many('sred_system.crm_targeting', 'targets', "targeting_profile_dna")

    def perform_manta_search(self, cr, uid, ids, context):
        return {
                  'type'     : 'ir.actions.act_url',
                  'target'   : 'new',
                  'url'      : 'http://www.manta.com'
               }



class my_changes_to_mail_templates(models.Model):
    _inherit = 'mail.template'

    code = fields.Html('code')

    @api.one
    def copy_body_to_code(self):
        self.code = self.body_html
        return

    @api.one
    def save_code_to_body(self):
        self.body_html = self.code


