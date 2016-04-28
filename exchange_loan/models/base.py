# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import time
import datetime
from dateutil.relativedelta import relativedelta

import openerp
from openerp import SUPERUSER_ID
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp import api, fields, models, _
from openerp.exceptions import UserError


class ResPartner(models.Model):
    """
    Display loans in partner form and add element for configuration
    specific to the partner
    """
    _inherit = 'res.partner'

    exchange_loan_ids = fields.One2many(
        'exchange.loan.contract', 'partner_id', 'Loans',
        help="Related loans")




