from openerp import models, fields, api, osv


#class my_crm_dna_types(models.Model):
#    _name = "sred_system.crm_dna_types"
#
#    dna_id = fields.One2Many('sred_system.crm_dna_tags', 'dna_type', 'targeting_tag')
#    sequence = fields.Integer()
#    name = fields.Char()


#class my_crm_targeting_tags(models.Model):
#    _name = "sred_system.crm_dna_tags"

#    dna_type = fields.Many2Ones('sred_system.crm_dna_types', 'dna_id')
#    name = fields.Char()
#    color = fields.Integer()

# Used to create a static targeting set information for leads and opportunitys that can be
# brought into a modified version of the existing crm

class my_crm_targeting_data(models.Model):
    _name = "sred_system.crm_targeting"

#    targets = fields.Many2One('crm.leads','target_profile')

    # Industry Codes
    naics = fields.Char()
    sred_code = fields.Char()

    # Business Data
    number_employees = fields.Integer()
    year_started     = fields.Integer()
    est_revenue      = fields.Float()

    # Various DNA Tags





