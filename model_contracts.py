from openerp import models, fields, api, osv



class my_sred_services_rates(models.Model):
    _inherit        = "sred_system.base_sred_object"
    _name           = "sred_system.sred_services_rates"
    _file_prefix    = 'SR'

    service_id      = fields.Many2one('sred_system.sred_services', string='contract service')
    amount_from     = fields.Float(digits=(10, 2))
    amount_to       = fields.Float(digits=(10, 2))
    commission_rate = fields.Float(digits=(2, 2))


class my_sred_services(models.Model):
    _inherit        = "sred_system.base_sred_object"
    _name           = 'sred_system.sred_services'
    _file_prefix    = "SS"

    name            = fields.Char()
    contracts       = fields.One2many('sred_system.sred_contracts', 'contracted_service', string='contracts')
    service_rates   = fields.One2many('sred_system.sred_services_rates', 'service_id', string='service rates')


class my_sred_contracts(models.Model):
    _inherit        = "sred_system.base_sred_object"
    _name           = 'sred_system.sred_contracts'
    _file_prefix    = "CA"

    contracted_service = fields.Many2one('sred_system.sred_services', string='contracted service')
    partner_id         = fields.Many2one('res.partner', string='partner')
    sales_person       = fields.Many2one('res.users', string='sales_person')
    claim_projects     = fields.One2many('sred_system.claim_project', 'id', string='claim_projects')
    yearly_term        = fields.Integer()
    date_signed        = fields.Datetime()
    date_expires       = fields.Datetime()

