# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber, Yannick Buron>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from openerp import models, fields, api
from openerp.exceptions import except_orm
from datetime import datetime, timedelta
import exchange_model

#    List/Model of Loans and Loans Type


class ExchangeLoanContractsTypes(models.Model):
    # Loans in form of System loans not private (p2p) ones
    # Process TODO
    _name = 'exchange.loan.contract.type'
    _description = 'Exchange Loans Types'
    _order = 'name'

    name = fields.Char('Type Name', size=64, translate=True, required=True)
    desc = fields.Text('Description', translate=True,)
    contract = fields.Text('Contract Text', translate=True,)
    account_from_id = fields.Many2one(
        'exchange.accounts', 'Account to rise loan', required=True)

    loan_contract_ids = fields.One2many(
        'exchange.loan.contract', 'loan_type_id',
        'Related Loan Contracts')
    loan_max_amount = fields.Float('Maximal amount of Loan')
    loan_revolving = fields.Boolean(
        'Is a revolving Loan type',
         help='A revolving does renew after each month')
    loan_grant_type_id = fields.One2many(
        'exchange.transaction.type', 'loan_contract_type_ids',
        'Loan transaction types')
#    loan_repayment_type_id = fields.Many2one(
#        'exchange.transaction.type',
#        'Loan repayment transaction type')
#    loan_interest_type_id = fields.Many2one(
#        'exchange.transaction.type',
#        'Loan interest transaction type')
#    loan_expiration_fee_type_id = fields.Many2one(
#        'exchange.transaction.type',
#        'Loan expiration fee transaction type')
    loan_monthly_interest = fields.Float('Loan monthly interest (%)')
    loan_grant_fee_value = fields.Float('Loan grant fee value')
    loan_expiration_fee_value = fields.Float('Loan expiration fee value')
    loan_repayment_days = fields.Integer('Loan repayment days')
    #Related feilds
    currency_from = fields.Many2one('res.currency',
        'Credit Currency', related='account_from_id.currency_base',
         readonly=True)


class ExchangeLoanContracts(models.Model):
    # Loans in form of System loans not private (p2p) ones
    # Process TODO
    _name = 'exchange.loan.contract'
    _description = 'Exchange Loans'
    _order = 'name,transaction_id'

    name = fields.Char('Loan Name', size=64, required=True)
    desc = fields.Text('Description')
    transaction_id = fields.One2many(
        'exchange.transaction', 'loan_contract_id',
        'Loan transactions',
         help='All transactions related to the loan')
    partner_id = fields.Many2one(
        'res.partner', 'Partner', ondelete='cascade',
         help='Partner/Customer who gets the loan')
    total_amount = fields.Float('Total amount of Loan')
    loan_type_id = fields.Many2one(
        'exchange.loan.contract.type',
        'Loan type',
         help='Related Loan type for this loan')
    loan_repayment_transaction_id = fields.Many2one(
        'exchange.transaction',
        'Loan repayment transaction')
    loan_interest_transaction_id = fields.Many2one(
        'exchange.transaction',
        'Loan interest transaction')
    loan_grant_fee_value = fields.Float('Loan grant fee value')
    loan_grant_fee_type = fields.Char('Loan grant fee type')
    loan_grant_fee_type_id = fields.Integer('Loan grant type id')
    loan_monthly_interest = fields.Float('Loan monthly interest (%)')
    loan_expiration_fee_value = fields.Float('Loan expiration fee value')
    loan_expiration_fee_type = fields.Char('Loan expiration fee type')
    loan_expiration_fee_type_id = fields.Integer('Loan expiration fee type id')
    loan_expiration_daily_interest = fields.Float('Loan expiration daily interest')
    loan_exp_daily_interest_type_id = fields.Integer('Loan expiration daily interest type id')
    loan_repayment_days = fields.Integer('Loan repayment days')
    state = fields.Selection(
            [
                ('draft', 'Draft'),
                ('active', '⌛Active'),
                ('delayed', 'Delayed'),
                ('done', 'Closed'),
                ('donedelayed', 'Closed delayed'),
                ('default', 'Defaulted'),
                ('cancel', 'Canceled'),
            ], 'Status', default='draft', required=True, track_visibility='onchange')

    # Related fields
    currency_from = fields.Many2one('res.currency',
        'Currency from', related='loan_type_id.currency_from',
         readonly=True)



