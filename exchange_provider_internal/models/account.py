# -*- coding: utf-'8' "-*-"

import json
import logging

from openerp import models, fields, api
from openerp.tools.float_utils import float_compare
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class ExchangeAccounts(models.Model):
    #    List of Accounts for members and the system
    _inherit = 'exchange.accounts'

    account_id_internal = fields.Many2one('exchange.account.provider.internal', 'Account link to Provider',
                                  track_visibility='onchange', required=False)


class ProviderAccount(models.Model):
    #    List of internal Accounts for members and the system
    _name = 'exchange.account.provider.internal'
    _description = 'Exchange Provider Accounts Internal'
    _order = 'template_id,name'

    @api.model
    def _get_limit_neg(self):
        return self.template_id.limit_negative

    @api.model
    def _get_limit_neg_val(self):
        return self.template_id.limit_negative_value

    @api.model
    def _get_limit_pos_val(self):
        print self.template_id.limit_positive_value
        return 50.0

    name = fields.Char('Account Name', size=64, required=True)
    provider_id = fields.Many2one(related='template_id.exchange_provider_id', string='Provider', required=False)
    template_id = fields.Many2one('exchange.config.accounts', 'Account Template',
                                  track_visibility='onchange', required=True)
    limit_negative = fields.Boolean('Limit - ?', default=_get_limit_neg)
    limit_negative_value = fields.Float('Credit Limit -', default=0.0)
    limit_positive = fields.Boolean('Limit + ?', default=True)
    limit_positive_value = fields.Float('Account Limit +', default=_get_limit_pos_val)

    # Computed fields
    balance = fields.Float(
        'Account Balance', store=False,
        compute='_get_balance')

    @api.one  # computed field balance calculate
    def _get_balance(self):

        self.balance = 1500.0

