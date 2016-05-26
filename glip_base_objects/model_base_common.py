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
    
                
    