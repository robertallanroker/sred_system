from openerp import models, fields, api, osv
from datetime import datetime, date
import time

#
#                          /---| WORK_TYPES
#                         /
#   WORK_RESOURCE_ROLES >|-----| WORK_RESOURCE_SCOPE
#           V             \
#           |              \---| WORK_FUNCTIONS
#           |
#           |-----------> SRED_PROJECT
#
#



