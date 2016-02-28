from openerp import models, fields, api, osv


# Contingency, Fixed, Etc.
class my_sred_services_modes(models.Model):
    _name    = 'sred_system.sred_service_modes'
    _inherit = 'sred_system.base_sred_picklist'

    name = fields.Char()
    mode = fields.Many2many('sred_system.sred_services', 'service_modes', 'mode')


class my_sred_services_rates(models.Model):
    _name           = "sred_system.sred_services_rates"
    _inherit        = "sred_system.base_sred_object"
    _file_prefix    = 'SR'

    service_id      = fields.Many2one('sred_system.sred_services', string='contract service')
    rate_mode       = fields.Many2one('sred_system.sred_service_modes', string='type of service')
    amount_from     = fields.Float(digits=(10, 2))
    amount_to       = fields.Float(digits=(10, 2))
    commission_rate = fields.Float(digits=(2, 2))


class my_sred_services(models.Model):
    _name           = 'sred_system.sred_services'
    _inherit        = "sred_system.base_sred_object"
    _file_prefix    = "SS"

    service_modes   = fields.Many2many('sred_system.sred_service_modes', 'mode', 'service_modes')
    contracts       = fields.One2many('sred_system.sred_contracts', 'contracted_service', string='contracts')
    service_rates   = fields.One2many('sred_system.sred_services_rates', 'service_id', string='service rates')


class my_sred_contracts(models.Model):
    _name           = 'sred_system.sred_contracts'
    _inherit        = "sred_system.base_sred_object"
    _file_prefix    = "CA"

    name               = fields.Char(readonly=True)
    active_mode        = fields.Many2one('sred_system.sred_service_modes', string='currently active service mode')
    contracted_service = fields.Many2one('sred_system.sred_services', string='contracted service')
    partner_id         = fields.Many2one('res.partner', string='partner')
    sales_person       = fields.Many2one('res.users', string='sales_person')
    claim_projects     = fields.One2many('sred_system.claim_project', 'id', string='claim_projects')
    yearly_term        = fields.Integer()
    date_signed        = fields.Datetime()
    date_expires       = fields.Datetime()

    @api.model
    @api.onchange('file_no')
    def on_changed_file_no(self):
        self.name = self.file_no
        return
