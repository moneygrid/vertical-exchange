# -*- coding: utf-'8' "-*-"

import json
import logging

from openerp import models, fields, api
from openerp.tools.float_utils import float_compare
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class ProviderAccount(models.Model):
    #    List of Accounts for members and the system
    _name = 'exchange.provider.internal'
    _description = 'Exchange Provider Accounts Internal'
    _order = 'template_id,name'

    @api.onchange('template_id')
    def _get_creditlimit(self):
        print self
        limitout = 9.0
        # template_id.limit_positive_value
        limitout = self.env['exchange.config.accounts'].browse(self._context.get('limit_positive_value'))
        print limitout
        self.limit_positive_value = limitout

    name = fields.Char('Account Name', size=64, required=True)
    provider_id = fields.Many2one(related='template_id.exchange_provider_id', string='Provider', required=False)
    template_id = fields.Many2one(
        'exchange.config.accounts', 'Account Template',
        track_visibility='onchange', required=True)
    limit_negative = fields.Boolean('Limit - ?')
    limit_negative_value = fields.Float(
        'Credit Limit -', default=0.0)
    limit_positive = fields.Boolean('Limit + ?')
    limit_positive_value = fields.Float(
        'Account Limit +')

    # Computed fields
    balance = fields.Float(
        'Account Balance', store=False,
        compute='_get_balance')

    @api.one # computed field balance calculate
    def _get_balance(self):

        self.balance = 1500.0

