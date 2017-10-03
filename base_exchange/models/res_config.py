# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber, Yannick Buron>
# based on account_wallet by Yannick Buron, Copyright Yannick Buron
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ExchangeConfigSettingsBak(models.Model):
    _name = 'exchange.config.data'
    """
    This model contains the config data of the transient model 'exchange.config.settings'
    """
    name = fields.Char(
        'Exchange Name', required=True, size=21, default='MY Exchange',
        help='Name of the Exchange')

    company_id = fields.Many2one(
        'res.company', 'Exchange Organisation',
        help="Organisation or Company that runs the Exchange")
    journal_id = fields.Many2one('account.journal', 'Community Journal', required=False)
    ref_currency_id = fields.Many2one(
        'res.currency', 'Reference currency',  # default=_default_currency,
        help="Currency which is used to calculate exchange rates for transaction engine /n"
             "ATTENTION Reference currency for Odoo Accounting my differ!", store=True,
        domain=[('exchange_currency', '=', True)], required=False)


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

    name = fields.Char('Exchange Name', required=True, size=21, default='MY Exchange',
                        help='Name of the Exchange')

    company_id = fields.Many2one('res.company', string='Exchange Organisation', required=True,
                                 default=lambda self: self.env.user.company_id,
                                 help="Organisation or Company that runs the Exchange")

    journal_id = fields.Many2one('account.journal', 'Community Journal', required=False)
    ref_currency_id = fields.Many2one(string='Reference currency', # default=_default_currency,
        help="Currency which is used to calculate exchange rates for transaction engine /n"
             "ATTENTION Reference currency for Odoo Accounting my differ!", store=True,
        domain=[('exchange_currency', '=', True)], required=False)

    module_exchange_loan = fields.Boolean("Install Loan module",
                                          help='-It installs the module exchange_loan.')
    module_exchange_membership = fields.Boolean("Install Membership module",
                                                help='-It installs the module exchange_membership.')


class ResCurrency(models.Model):
    """
    Add a boolean field in currency to identify currency usable in wallet/exchange
    """
    _inherit = 'res.currency'

    exchange_currency = fields.Boolean('Exchange currency?', readonly=False)

