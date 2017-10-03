# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber, Yannick Buron>
# based on account_wallet by Yannick Buron, Copyright Yannick Buron
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging
from odoo import api, fields, models
# from odoo.tools import image
_logger = logging.getLogger(__name__)


class ExchangeConfigSettings(models.TransientModel):

    """
    Exchange settings which are related to the different Providers
    """
    _inherit = 'exchange.config.settings'

    exchange_provider_id = fields.Many2one('exchange.provider', 'Exchange Provider',
                                          help='Related Transaction engine internal or external')

    exch_code = fields.Char(
        'Exchange Code', related='exchange_provider_id.exch_code',
        help="Unique Exchange Code (EC)"
             "First part of the 20 digits Account Code CC BBBB"
             "CC country code -> DE Germany"
             "BBBB Exchange code")

    # Related fields
    is_external = fields.Boolean(string='External Provider', related='exchange_provider_id.is_external')
    display_balance = fields.Boolean('Everyone can see balances?',
                                     related='exchange_provider_id.display_balance')
    use_account_numbers = fields.Boolean(
        'Use of Account Numbering System', related='exchange_provider_id.use_account_numbers',
        help="Use of the 20 digits Account Numbering Code 'CC BBBB DDDDDDDD XXXX-KK'")
    email_sysadmin = fields.Char('Sysadmin mail address', related='exchange_provider_id.email_sysadmin')
    # account_conf_ids = fields.One2many('Accounts templates', related='exchange_provider_id.account_conf_ids')


class ResPartner(models.Model):
    """
    Display accounts in partner form and add element for configuration
    specific to the partner
    """
    _inherit = 'res.partner'
    """
    @api.model
    @api.depends('exchange_provider_id')
    def _default_exchange_provider(self):
        settings = self.env['exchange.config.settings']  # TODO .search([('exchange_provider_id', '>', 0)])
        provider_id = {}
        for record in settings:
            provider_id = settings.mapped('exchange_provider_id')
        print "provider id", settings, provider_id
    """
    @api.model
    @api.depends('exchange_provider_id')
    def _default_see_balance(self):
        #  see_balance = self.exchange_provider_id.display_balance
        return True

    exchange_account_ids = fields.One2many(
        'exchange.accounts', 'partner_id', 'Accounts',
        help="Related accounts to this user")
    create_date = fields.Datetime('Create date')
    see_balance = fields.Boolean('Can see balance?', default=_default_see_balance)
    exchange_provider_id = fields.Many2one(
        'exchange.provider', 'Exchange Provider', required=False)  #  TODO ,  default=_default_exchange_provider,
    exchange_user_code = fields.Char(
        'Exchange Client Code', compute='_compute_user_code', size=13,
        readonly=False, store=True)
    exchange_user_token = fields.Char(
        'Client Token', compute='_compute_user_token', size=128,
        readonly=False, store=True)

    @api.multi
    @api.depends('exchange_provider_id')
    def _compute_user_icann_code(self):
        """
        Computes the Exchange code (Membership number) of the user according the ICANN speficiations.

        self.ensure_one()  # One record expected, raise error if self is an unexpected recordset
        exch_code = self.exchange_provider_id.exch_code
        partid = 1235  # TODO
        type1 = str(exch_code + '-' + partid)
        print partid, type1
        return type1
        """
    @api.multi
    @api.depends('exchange_user_code')
    def _compute_user_code(self):
        """
        Computes the user token (Membership number) as a Hash from the exchange_user_code.
        """
        self.ensure_one()  # One record expected, raise error if self is an unexpected recordset
        # user_code_hash = base.hash_string(self.exchange_user_code)
        # print "user Hash", user_code_hash
        return "default-code"

    @api.multi
    @api.depends('exchange_user_token')
    def _compute_user_token(self):
        """
        Computes the user token (Membership number) as a Hash from the exchange_user_code.
        """
        self.ensure_one()  # One record expected, raise error if self is an unexpected recordset
        # user_code_hash = base.hash_string(self.exchange_user_code)
        # print "user Hash", user_code_hash
        return 3159889080830


