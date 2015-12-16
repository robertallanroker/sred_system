from openerp import models, fields, api, osv
from datetime import datetime, date
import time


class my_documentation_labels(models.Model):
    _name = 'sred_system.documentation_labels'
    name = fields.Char()
    doc_label_id = fields.Many2many('sred_system.documentation', 'document_id', 'doc_label_id')
    sequence    = fields.Integer(default=10)
    is_default  = fields.Boolean(default=False)


class my_documentation(models.Model):
    _name = 'sred_system.documentation'
    name = fields.Char()
    document_id = fields.Many2many('sred_system.documentation_labels', 'doc_label_id', 'document_id')
    document_tags = fields.Many2many('sred_system.documentation_tags', 'doctags_id', 'document_tags')
    sred_project = fields.Many2many('sred_system.sred_project', 'documentation', 'sred_project')
    sequence    = fields.Integer(default=10)
    is_default  = fields.Boolean(default=False)


class my_documentation_tags(models.Model):
    _name = 'sred_system.documentation_tags'
    name = fields.Char()
    doc_tags_id = fields.Many2many('sred_system.documentation','document_tags', 'doc_tags_id')
    sequence    = fields.Integer(default=10)
    is_default  = fields.Boolean(default=False)