from openerp import models, fields, api, osv
from datetime import datetime, date
import time

class my_work_folders(models.Model):
    _inherit            = 'sred_system.base_sred_object'
    _name               = 'sred_system.work_folders'
    name                = fields.Char()
    num_sred_projects   = fields.Integer()
    Folder_id           = fields.One2many('sred_system.sred_project', 'an_assigned_folder', ondelete='cascade')
    folder_fee_booked   = fields.Float()
    folder_fee_filed    = fields.Float()
    folder_fee_refund   = fields.Float()
    is_active           = fields.Boolean(default=True)

    @api.one
    @api.model
    def _calculate_fees(self):
        fee_amount_booked = 0.00
        fee_amount_filed  = 0.00
        fee_amount_refund = 0.00
        if self.Folder_id:
            for my_rec in self.Folder_id:
                fee_amount_booked = fee_amount_booked + my_rec.Estimated_Fee
                fee_amount_filed  = fee_amount_filed  + my_rec.Estimated_Fee
                fee_amount_refund = fee_amount_refund + my_rec.Estimated_Refund
                self._say(my_rec.Estimated_Refund)
                self._say(fee_amount_booked)
                self._say(fee_amount_filed)
        self.folder_fee_booked = fee_amount_booked
        self.folder_fee_filed  = fee_amount_filed
        self.folder_fee_refund = fee_amount_refund


    @api.one
    @api.onchange('Folder_id')
    def _calculate_folder_fees(self):
       self._calculate_fees()
