from openerp import models, fields, api, osv
from random import randint
from datetime import datetime, date
import time


class my_glip_base_common(models.Model):
    _name      = "glip.base.common"
    _res_model = _name


    # LINK RECORD
    # Link the current record to the specified res_model and res_id
    @api.one
    def link_record (self, this_res_model, this_res_id):
        if this_res_model:
            if this_res_id:
                self.res_model = this_res_model
                self.res_id    = this_res_id
        return
    
    @api.multi
    def get_current_record(self):
        this_id         = self.ids
        this_record     = self.env[self._name].browse(this_id)
        return this_record
    
    @api.model
    def get_date_year(self, this_date):
        return getattr(this_date,'year')
    
    @api.model
    def get_date_month(self, this_date):
        return getattr(this_date,'month')
    
    @api.model
    def get_date_day(self, this_date):
        return getattr(this_date,'day')
    
    @api.model
    def is_this_week(self, this_date):
        this_today = datetime.datetime.now().strftime('%m-%d-%Y') 
        this_day = self.get_date_day(this_today)
        this_val = self.get_date_day(this_date)
        return this_val == this_day
    
    @api.model
    def is_this_month(self, this_date):
        this_today = datetime.datetime.now().strftime('%m-%d-%Y') 
        this_month = self.get_date_month(this_today)
        this_val   = self.get_date_month(this_date)
        return this_month == this_val
    
    @api.model
    def is_this_year(self, this_date):
        this_today = datetime.datetime.now().strftime('%m-%d-%Y')
        this_year = self.get_date_year(this_date)
        this_val  = self.get_date_year(this_today)
        return this_year == this_val