# -*- coding: utf-8 -*-
from openerp import http

# class SredSystem(http.Controller):
#     @http.route('/sred_system/sred_system/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sred_system/sred_system/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sred_system.listing', {
#             'root': '/sred_system/sred_system',
#             'objects': http.request.env['sred_system.sred_system'].search([]),
#         })

#     @http.route('/sred_system/sred_system/objects/<model("sred_system.sred_system"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sred_system.object', {
#             'object': obj
#         })