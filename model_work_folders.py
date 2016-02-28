from openerp import models, fields, api, osv
from datetime import datetime, date
import time



class my_sred_tax_years(models.Model):
    _inherit    = 'sred_system.base_sred_picklist'
    _name       = 'sred_system.tax_years'
    name        = fields.Char()
    taxyear_id  = fields.Many2many('sred_system.claim_project','tax_years','taxyear_id')




class my_work_folder_groups(models.Model):
    _inherit            = 'sred_system.base_sred_picklist'
    _name               = 'sred_system.folder_groups'
    sred_claim          = fields.One2many('sred_system.claim_project', 'folder_group', 'relation to claims', ondelete='cascade')


class my_work_folders(models.Model):
    _inherit            = 'sred_system.base_sred_picklist'
    _name               = 'sred_system.work_folders'
    name                = fields.Char()

    num_sred_projects   = fields.Integer(compute='count_claims')
    folder_id           = fields.One2many('sred_system.claim_project', 'folder', ondelete='cascade')



    _defaults = {'is_active':True}