from openerp import models, fields, api, osv
from openerp.tools.translate import _


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

    name               = fields.Char()
    active_mode        = fields.Many2one('sred_system.sred_service_modes', string='currently active service mode')
    contracted_service = fields.Many2one('sred_system.sred_services', string='contracted service', required=True)
    partner_id         = fields.Many2one('res.partner', string='customer', required=True, domain=[('customer','=',True)])
    sales_person       = fields.Many2one('res.users', string='sales_person', required=True)
    claim_projects     = fields.One2many('sred_system.claim_project', 'contracted_service', string='claim_projects')
    yearly_term        = fields.Integer()
    date_signed        = fields.Datetime()
    date_expires       = fields.Datetime()
    contract_docs      = fields.One2many('ir.attachment', 'res_id',
                                         domain  = lambda self: [('res_model', '=', self._name), ('res_id','=', self.id)],
                                         string  = 'contract document')
    doc_count          = fields.Integer(compute = "_get_attached_docs", string = "Number of contracts attached", type='integer')
    year_end           = fields.Datetime(related='partner_id.cra_year_end', string = "Year End")


    def attachment_tree_view(self, cr, uid, ids, context):
        task_ids = self.pool.get('sred_system.sred_contracts').search(cr, uid, [('id', 'in', ids)])
        domain = [('res_model', '=', 'sred_system.sred_contracts'), ('res_id', 'in', ids)]
        res_id = ids and ids[0] or False
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Signed contract documents are attached to the contract profile record.</p>
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, res_id)
        }

    @api.one
    def _get_attached_docs(self):
        my_obj = self.env["ir.attachment"]
        my_docs = my_obj.search([('res_model','=','sred_system.sred_contracts'), ('res_id','=', self.id)])
        if my_docs:
            self.doc_count = len(my_docs)
        else:
            self.doc_count = 0
        return

    _defaults = {'name':'Standard Contract'}