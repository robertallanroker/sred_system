from openerp import models, fields, api, osv


class my_changes_to_customers(models.Model):
     _inherit = 'res.partner'

     cra_bin = fields.Char()
     cra_year_end = fields.Datetime()

     service_contracts = fields.One2many('sred_system.sred_contracts', 'contracted_service', string='service_contracts')

     # You should make the default partner record automatically a customer. Especially when you are using CRM and
     # loading lots of non-customer accounts.
     _defaults = {'is_customer': False}


#class my_fix_to_silly_im_chat_bug(models.Model):
#    _inherit = 'im_livechat.channel'

    # RAR - Quick Fix Bug Work Around, completly missing this method from code.
    # I have no idea what this function is supposed to do and why its being called while trying to upgrade module.
#    def match_rules(self, channel_id, url, country_id=False):
#        if self.rule_id:
#            for my_rule in self.rule_ids:
#                my_rule.match_rule(channel_id, url, country_id=False)
#        return False

