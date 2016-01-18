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

    f_new                     = fields.Float(compute='_calc_new')
    f_processed               = fields.Float(compute='_calc_processed')
    f_booked                  = fields.Float(compute='_calc_booked')
    f_total                   = fields.Float(compute='_calc_total')
    f_progress                = fields.Float(compute='_calc_f_progress')
    folder_fee_new          = fields.Float()
    folder_fee_processed    = fields.Float()
    folder_fee_booked       = fields.Float()
    folder_fee_total        = fields.Float()

    progress                = fields.Float()

    is_active = fields.Boolean()


    @api.one
    @api.model
    def count_claims(self):
        return len(self.folder_id)

    @api.one
    @api.model
    @api.onchange('folder_fee_total')
    def _calc_total(self):
        self.f_total = self.folder_fee_total
        return self.folder_fee_total

    @api.one
    @api.model
    @api.onchange('folder_fee_new')
    def _calc_new(self):
        self.f_new = self.folder_fee_new
        return self.folder_fee_new

    @api.one
    @api.model
    @api.onchange('folder_fee_processed')
    def _calc_processed(self):
        self.f_processed = self.folder_fee_processed
        return self.folder_fee_processed

    @api.one
    @api.model
    @api.onchange('folder_fee_booked')
    def _calc_booked(self):
        self.f_booked = self.folder_fee_booked
        return self.folder_fee_booked

    @api.one
    @api.model
    @api.onchange('progress')
    def _calc_f_progress(self):
        self.f_progress = self.progress
        return self.f_progress


    @api.one
    @api.model
    def _calc_progress(self):
        ppp = self.folder_fee_processed
        eee = self.folder_fee_total
        np  = 0
        if eee > 0:
            np = ppp / eee
        self.progress = np
        return np


    @api.one
    @api.model
    def calculate_fees(self):
        calc_fee  = {}
        if self.folder_id:
            for my_rec in self.folder_id:
                # avoid double counting revenue, so pick from list of revenue preferences
                rev_list = ['a1']
                calc_fee['a1'] = 0.00
                calc_fee['a2'] = 0.00
                calc_fee['a3'] = 0.00
                if my_rec.cra_processing_status.revenue:
                    rev_list.append(my_rec.cra_processing_status.revenue)
                if my_rec.glip_processing_status.revenue:
                    rev_list.append(my_rec.glip_processing_status.revenue)
                if my_rec.work_processing_status.revenue:
                    rev_list.append(my_rec.work_processing_status.revenue)
                # Preference grab fee types
                if 'a3' in rev_list:
                    calc_fee['a3'] = my_rec.estimated_fee
                elif 'a2' in rev_list:
                    calc_fee['a2'] = my_rec.estimated_fee
                elif 'a1' in rev_list:
                    calc_fee['a1'] = my_rec.estimated_fee
                elif 'a4' in rev_list:
                    calc_fee['a4'] = my_rec.estimated_fee

        if calc_fee:
            self.folder_fee_new       = calc_fee['a1']
            self.folder_fee_booked    = calc_fee['a3']
            self.folder_fee_processed = calc_fee['a2']
            self.folder_fee_total     = (calc_fee['a1'] + calc_fee['a2'] + calc_fee['a3'])
        self._calc_progress


    @api.one
    @api.onchange('Folder_id')
    def _calculate_folder_fees(self):
       self.calculate_fees()
       self.count_folders()


    @api.one
    @api.model
    def open_project_claim(self):
        result = {
            "type": "ir.actions.act_window",
            "res_model": "sred_system.claim_project",
            "view_type": "form",
            "target": "current",
#            "domain": [('id', '=', claim_project_id)],
#            "context":
            "context": context,
            "name": "SRED Project",
            "nodestroy": True}
        return result


    _defaults = {'is_active':True}