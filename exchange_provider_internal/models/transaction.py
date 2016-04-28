# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber, Yannick Buron>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import models, fields, api
from openerp.exceptions import except_orm
from datetime import datetime, timedelta

#    TODO Models of Transfers in internal transaction engine, so far in module exchange_provider solved


class ExchangeMove(models.Model):
    """
    Object to generate Transfer Entries, who stores all the communication between .
    sender and receiver accounts. Type of information are:
    'Transfer' -> sending money
    'Invoice'  -> sending invoice
    'Invoice Confirm'
    'Transfer to Confirm' -> ??????
    'Confirmation'
    'Info' -> only message
    """
    _inherit = 'exchange.transaction.line'


    @api.multi
    def get_account_balance(self, account_id,  transfer_type, context=None):
        # Compute balances for specified partner account
        if not context:
            context = {}
        ctx = context.copy()
        sum_from = self.amount_from
        sum_to = self.amount_from

        return sum_to - sum_from

    @api.one
    def get_field(self, field):
        # get field from transaction model
        # TBS does not work

        # trans_line = self.env['exchange.transaction']
        # result = trans_line.field
        result = 1
        print field
        print result
        return result


class ExchangeTransactions(models.Model):
    """
    Main object used for the workflow of transferring values, invoices and messages , from sender_account to receiver_account    It has his own workflow, from draft to paid and can be refund.

    """
    _inherit = 'exchange.transaction'

