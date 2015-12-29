from openerp import models, fields, api, osv
from datetime import datetime, date
import time

class my_work_folders(models.Model):
    _inherit            = 'sred_system.base_sred_object'
    _name               = 'sred_system.work_folders'
    name                = fields.Char()
    num_sred_projects   = fields.Integer(compute='count_folders')
    Folder_id           = fields.One2many('sred_system.sred_project', 'an_assigned_folder', ondelete='cascade')
    folder_fee_new          = fields.Float()
    folder_fee_processed    = fields.Float()
    folder_fee_booked       = fields.Float()
    is_active               = fields.Boolean()
    _defaults = {'is_active':True}

    @api.one
    @api.model
    def count_folders(self):
        num_f = 0
        if self.Folder_id:
            num_f = len(self.Folder_id)
        self.num_sred_projects = num_f
        return num_f

    @api.one
    @api.model
    def calculate_fees(self):
        fee_amount_new       = 0.00
        fee_amount_booked    = 0.00
        fee_amount_processed = 0.00
        if self.Folder_id:
            for my_rec in self.Folder_id:
                found_slot = False
                if 'a1' in my_rec.sred_cra_status.revenue:
                    fee_amount_new += my_rec.Estimated_Fee
                    found_slot = True
                if 'a2' in my_rec.sred_cra_status.revenue:
                    fee_amount_processed += my_rec.Estimated_Fee
                    found_slot = True
                if 'a3' in my_rec.sred_cra_status.revenue:
                    fee_amount_booked += my_rec.Estimated_Fee
                    found_slot = True
                if not found_slot:
                    if 'a1' in my_rec.sred_processing_status.revenue:
                        fee_amount_new += my_rec.Estimated_Fee
                    if 'a2' in my_rec.sred_processing_status.revenue:
                        fee_amount_processed += my_rec.Estimated_Fee
                    if 'a3' in my_rec.sred_processing_status.revenue:
                        fee_amount_booked += my_rec.Estimated_Fee
        self.folder_fee_new       = fee_amount_new
        self.folder_fee_booked    = fee_amount_booked
        self.folder_fee_processed = fee_amount_processed

    @api.one
    @api.onchange('Folder_id')
    def _calculate_folder_fees(self):
       self.calculate_fees()
       self.count_folders()

