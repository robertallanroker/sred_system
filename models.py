# -*- coding: utf-8 -*-
from openerp import models, fields, api, osv
from datetime import datetime, date
import time

#
# MODIFICATIONS TO PROJECT ENTITIES
#

class my_uncertainties(models.Model):
    _name= 'sred_system.uncertainties'
    name = fields.Char()
    uncertainties_id = fields.Integer()
    description = fields.Char()

class my_hypothesis(models.Model):
    _name= 'sred_system.hypothesis'
    name = fields.Char()
    Is_Active = fields.Boolean()
    List_of_uncertainties = fields.Integer()

class my_milestones(models.Model):
    _name = 'sred_system.milestones'
    name = fields.Char()




## No need? Have Documentation Types now?
class my_ObjectiveEvidence_types(models.Model):
    _name = 'sred_system.objective_evidence_types'
    name = fields.Char()

