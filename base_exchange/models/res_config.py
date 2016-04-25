# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber, Yannick Buron>
# based on account_wallet by Yannick Buron, Copyright Yannick Buron
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging
from openerp.tools import image_get_resized_images, image_resize_image_big
_logger = logging.getLogger(__name__)
from openerp import api, fields, models, _
from openerp.exceptions import UserError


class ExchangeConfigSettings(models.TransientModel):
    _name = 'exchange.config.settings'
    _inherit = 'res.config.settings'

    @api.model
    def _default_company(self):
        company_id = self.env.ref('base.main_company')
        return company_id

    @api.one
    @api.depends('company_id')
    def _get_currency_id(self):
        self.currency_id = self.company_id.currency_id

    @api.one
    def _set_currency_id(self):
        if self.currency_id != self.company_id.currency_id:
            self.company_id.currency_id = self.currency_id

    name = fields.Char(
        'Exchange Name', required=True, size=21, default='MY Exchange',
        help='Name of the Exchange')

    res_company_id = fields.Many2one(
        'res.company', 'Exchange Organisation', default=_default_company,
        help="Organisation or Company that runs the Exchange")
    display_balance = fields.Boolean('Everyone can see balances?', default=True)
    journal_id = fields.Many2one('account.journal', 'Community Journal', required=False)
    ref_currency_id = fields.Many2one(
        'res.currency', 'Reference currency', # default=_default_currency,
        help="Currency which is used to calculate exchange rates for transaction engine /n"
             "ATTENTION Reference currency for Odoo Accounting my differ!", store=True,
        domain=[('exchange_currency', '=', True)], required=False)
    use_account_numbers = fields.Boolean(
        'Use of Account Numbering System', default=True,
        help="Use of the 20 digits Account Numbering Code 'CC BBBB DDDDDDDD XXXX-KK'")
    email_sysadmin = fields.Char('Sysadmin mail address')


class ExchangeConfigSettings(models.TransientModel):
    """
    Exchange settings which will be used to configure the basic settings
    """
    _name = 'exchange.test.config.settings'
    # _description = 'Exchange configuration'

    _inherit = 'res.config.settings'


@api.model
def _default_company(self):
    company_id = self.env.ref('base.main_company')
    return company_id
"""

@api.model
def _default_journal(self):  # TODO default=_default_journal,
    journal_id = self.env.ref('base_exchange.exchange_journal_o1')
    return journal_id


@api.model
def _default_currency(self):
    currency_id = self.env.ref('base_exchange.DOO')
    return currency_id
"""

name = fields.Char(
    'Exchange Name', required=True, size=21, default='MY Exchange',
    help='Name of the Exchange')
exch_code = fields.Char(
    'Exchange Code', required=False, size=7, default='CH-EXCH01',
    help="Unique Exchange Code (EC)"
         "First part of the 20 digits Account Code CC BBBB"
         "CC country code -> DE Germany"
         "BBBB Exchange code")
res_company_id = fields.Many2one(
    'res.company', 'Exchange Organisation', default=_default_company,
    help="Organisation or Company that runs the Exchange")
display_balance = fields.Boolean('Everyone can see balances?', default=True)
journal_id = fields.Many2one('account.journal', 'Community Journal', required=False)
"""
account_ids = fields.One2many(
    'exchange.config.accounts', 'config_id', 'Accounts templates')
# TODO may raise conflicts with exchange rates in accounting system
"""
ref_currency_id = fields.Many2one(
    'res.currency', 'Reference currency', # default=_default_currency,
    help="Currency which is used to calculate exchange rates for transaction engine /n"
         "ATTENTION Reference currency for Odoo Accounting my differ!", store=True,
    domain=[('exchange_currency', '=', True)], required=False)
use_account_numbers = fields.Boolean(
    'Use of Account Numbering System', default=True,
    help="Use of the 20 digits Account Numbering Code 'CC BBBB DDDDDDDD XXXX-KK'")
email_sysadmin = fields.Char('Sysadmin mail address')


class ResCurrency(models.Model):
    """
    Add a boolean in currency to identify currency usable in wallet/exchange
    """
    _inherit = 'res.currency'

    exchange_currency = fields.Boolean('Exchange currency?', readonly=False)

