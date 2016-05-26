from openerp import models, fields, api, osv
from random import randint
from datetime import datetime, date
import time


class my_glip_base_heirarchy_list(models.Model):
    _name      = "glip.base.common"
    _inherit   = "glip.base.hierarchy_list"
    _seperator = "/"

    parent_id  = fields.Integer(default=False)
    label      = fields.Char(default='')
    depth      = fields.Integer(default=0)
    
    
    @api.one
    def _get_parent_name(self, this_parent_id):
        this_parent_record = self.env[self._name].browse(this_parent_id)
        this_parent_name   =  ""
        if this_parent_record:
            this_parent_name = this_parent_record.name
        return this_parent_name
    
    
    @api.one
    def _make_heirarchy_name(self, this_parent_id, this_label):
        return self._get_parent_name(self.parent_id) + self._seperator + this_label
        
    
    @api.onchange('parent_id')
    def _on_parent_id_changed(self):
        self.name           = self._make_heirachy_name(self.parent_id, self.label)
        this_parent_record  = self.env[self._name].browse(self.parent_id)
        if this_parent_record:
            self.depth = this_parent_record.depth + 1
        else:
            self.depth = 0
        return 
    
    
    @api.onchange('label')
    def _on_label_changed(self):
        self.name = self._make_heirarchy_name(self.parent_id, self.label)
        
        
        