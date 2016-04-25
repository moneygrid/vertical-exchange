# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber, Yannick Buron>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import models, fields, api
from openerp.exceptions import except_orm
from datetime import datetime, timedelta

#    Models of Transaction Types and Transfers

class ExchangeTransactionTypes(models.Model):
    """
    Object to generate Transaction Types, who defines which connection sender   .
    to receiver accounts are allowed and what are the rules.
    """
    _inherit = 'exchange.transaction.type'

    # TODO Loan fields/process not yet clear?
    is_loan = fields.Boolean('Is a loan transaction',
            help='Is a loan/grant transaction type')
    loan_contract_type_ids = fields.Many2one(
        'exchange.loan.contract.type',
        'Loan Contract Type', required=False,
        help='Related type of loan to this loan transaction')
    loan_tr_type = fields.Selection(
            [
                ('grant', 'Grant'),
                ('init_fee', 'Initial fee'),
                ('expiration_fee', 'Expiration fee'),
                ('interest', 'Interest'),
                ('repayment', 'Repayment'),
            ], 'Loan Status', readonly=False, required=False, track_visibility='onchange')


class ExchangeTransactions(models.Model):
    """
    Main object used for the workflow of transferring values, invoices and messages , from sender_account to receiver_account    It has his own workflow, from draft to paid and can be refund.

    """

    _inherit = 'exchange.transaction'

    is_loan = fields.Boolean('Is a loan transaction', track_visibility='onchange')
    loan_contract_id = fields.Many2one(
        'exchange.loan.contract', 'Related Loan contract', state={'draft': [('readonly', False)]}, required=False)
