from openerp import models, fields, api, osv

class my_mods_to_projects(models.Model):
    _inherit = 'project.project'
    sred_claim_project = fields.One2many('sred_system.sred_project','a_claim_project',  ondelete='cascade')

