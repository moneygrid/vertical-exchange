# -*- coding: utf-'8' "-*-"

import json
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ExchangeAccounts(models.Model):
    """
    Inherited model of Accounts for members and the system.
    Most of the here defined fields are related to the submodels exchange.account.provider.xxxxx!
    """
    _inherit = 'exchange.accounts'

    # All Computed fields
    limit_negative = fields.Boolean('Limit - ?', compute='_compute_limit_negative')
    limit_negative_value = fields.Float('Credit Limit -')
    limit_positive = fields.Boolean('Limit + ?')
    limit_positive_value = fields.Float('Account Limit +')
    """
    limit_negative = fields.Boolean('Limit - ?', related='account_id_internal.limit_negative')
    limit_negative_value = fields.Float('Credit Limit -', related='account_id_internal.limit_negative_value')
    limit_positive = fields.Boolean('Limit + ?', related='account_id_internal.limit_positive')
    limit_positive_value = fields.Float('Account Limit +', related='account_id_internal.limit_positive_value')
    """
    provider_ref = fields.Reference([
            ('exchange.account.provider.internal', 'Internal'),
            ('exchange.account.provider.dumy', 'Dumy')],
            'Ref test')
    available = fields.Float('Available', store=True, compute='_compute_available_amount')
    balance = fields.Float('Account Balance', store=False) # , compute='_compute_balance')
    reserved = fields.Float('Reserved')
    exchange_provider = fields.Selection('Exchange Provider', related='template_id.exchange_provider_id.provider',
                                         readonly=True, help='Related transaction engine name')
    transaction_view = fields.Selection([
            ('ingoing', 'Ingoing Transactions'),
            ('outgoing', 'Outgoing Transactions'),
            ('inout', 'All Transactions')],
            string='Transactions Filter', default='inout', help="Choose which transactions you like to see.")
    transaction_from_ids = fields.One2many('exchange.transaction', 'account_from_id', string='Transactions from')
    transaction_to_ids = fields.One2many('exchange.transaction', 'account_to_id', string='Transactions to')
    transaction_ids = fields.One2many('exchange.transaction', 'account_to_from_id',
                                      string='Transactions all', compute='_compute_transaction_ids')

    @api.multi  # TODO
    @api.depends('transaction_view', 'transaction_from_ids', 'transaction_to_ids')
    def _compute_transaction_ids(self):
        # ingoing = self.env['exchange.transaction'].search([('id', '=', self.id)])
        ingoing = self.transaction_from_ids
        outgoing = self.transaction_to_ids
        inout = ingoing + outgoing
        self.transaction_ids = inout
        return inout

    @api.one  # TODO auto switching of account_id_xxxxxxx
    def _compute_limit_negative(self):
        return self.account_id_internal.limit_negative

    @api.one  # Action connection test via the provider models
    def _compute_limit_negative2(self):
        sub_function = "_get_limit_negative_" + str(self.exchange_provider)
        call_limit = getattr(self, sub_function)
        result = call_limit()

    @api.one
    @api.depends('balance', 'limit_negative_value')  # computed field available calculate
    def _compute_available_amount(self):
        return float(self.balance - self.limit_negative_value)

    @api.one  # computed field balance calculate
    def _compute_balance(self):
        balance_internal = fields.Float('Account Balance', related='account_id_internal.balance')
        return balance_internal

    @api.one  # TODO get account_balance from test account
    def act_account_compute_balance(self):
        raise Exception("This is not yet implemented!")


class AccountTemplateConfig(models.Model):
    # Lines containing the general configuration of account templates
    _inherit = 'exchange.config.accounts'

    @api.onchange('exchange_provider_id')
    def _get_template_name(self):
        self.image = self.exchange_provider_id.image

    @api.multi
    def _compute_external(self):
        if 1 == 1:  # self.exchange_provider_id.environment == "internal":
            return False
        else:
            return True

    exchange_provider_id = fields.Many2one('exchange.provider', 'Exchange Provider',
                                           help='Related transaction engine internal or external')
    is_external = fields.Boolean(compute='_compute_external', string='External Account')
    """
    config_id = fields.Many2one(
        'exchange.config.settings', 'Config ID', required=False)
    """
    initcredit_type = fields.Many2one('exchange.transaction.type', 'Initial credit transaction type')

"""
_sql_constraints = [
    ('default_account', 'unique(membership_type,default_account,exchange_provider_id)',
     'We can only have one default account per type'),
    ]
"""