# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber, Yannick Buron>
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
    Display accounts in partner form and add element for configuration
    specific to the partner
    """
    _inherit = 'res.partner'

    @api.model
    def _default_exchange(self):
        exchange_id = self.env.ref('base.main_company')
        return exchange_id

    exchange_account_ids = fields.One2many(
        'exchange.accounts', 'partner_id', 'Accounts',
        help="Related accounts to this user")
    create_date = fields.Datetime('Create date')
    see_balance = fields.Boolean('Can see balance?', default='True')
    exchange_id = fields.Many2one(
        'exchange.config.settings', 'Exchange', required=False)  # TODO , default=_default_exchange
    exchange_user_code = fields.Char(
        'Exchange Client Code', compute='_compute_number', size=13,
        readonly=False, store=True)


@api.multi
def _compute_number(self):
    self.ensure_one()  # One record expected, raise error if self is an unexpected recordset
    code = 'CH-EXC1'
    partid = '0011'

    type1 = str(code + '-' + partid)
    print partid, type1
    return type1



