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


class ExchangeConfigSettings(models.Model):

    # Add Exchange configuration (parameters) to Exchange settings
    _inherit = 'exchange.config.settings'

    @api.model
    def _default_company(self):
        company_id = self.env.ref('base.main_company')
        return company_id

    @api.model
    def _default_journal(self):  # TODO default=_default_journal,
        journal_id = self.env.ref('exchange.exchange_journal_o1')
        return journal_id

    @api.model
    def _default_currency(self):
        currency_id = self.env.ref('base_exchange.DOO')
        return currency_id

    name = fields.Char(
        'Exchange Name', required=True, size=21, default='MY Exchange',
        help='Name of the Exchange')
    code = fields.Char(
        'Exchange Code', required=False, size=7, default='CH-EXCH01',
        help="Unique Exchange Code (EC)"
             "First part of the 20 digits Account Code CC BBBB"
             "CC country code -> DE Germany"
             "BBBB Exchange code")
    res_company_id = fields.Many2one(
        'res.company', 'Exchange Organisation',  default=_default_company,
        help="Organisation or Company that runs the Exchange")
    display_balance = fields.Boolean('Everyone can see balances?', default=True)
    journal_id = fields.Many2one('account.journal', 'Community Journal', required=False)
    account_ids = fields.One2many(
        'exchange.config.accounts', 'config_id', 'Accounts templates')
    # TODO may raise conflicts with exchange rates in accounting system
    ref_currency_id = fields.Many2one(
        'res.currency', 'Reference currency', default=_default_currency,
        help="Currency which is used to calculate exchange rates for transaction engine /n"
             "ATTENTION Reference currency for Odoo Accounting my differ!", store=True,
        domain=[('exchange_currency', '=', True)], required=False)
    use_account_numbers = fields.Boolean(
        'Use of Account Numbering System', default=True,
        help="Use of the 20 digits Account Numbering Code 'CC BBBB DDDDDDDD XXXX-KK'")
    email_sysadmin = fields.Char('Sysadmin mail address')


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
    exchange_loan_ids = fields.One2many(
        'exchange.loan.contract', 'partner_id', 'Loans',
        help="Related loans")
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



