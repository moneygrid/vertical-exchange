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
    _name = 'exchange.transaction.type'
    _description = 'Exchange Transactions Types'
    _order = 'name,from_account_type_id'

    name = fields.Char('Type Name', size=64, translate=True, required=True)
    desc = fields.Text('Description', translate=True)
    from_account_type_id = fields.Many2one(
        'exchange.config.accounts', 'Account From', required=True)
    to_account_type_id = fields.Many2one(
        'exchange.config.accounts', 'Account To', required=True)
    hidden = fields.Boolean('Hidden Transaction Type',
            help='Transactions Type is hidden to users')
    allowed_payment = fields.Boolean('Allowed Payment')
    allowed_self_payment = fields.Boolean('Allowed Self Payment')
    priority = fields.Boolean('Priority',
            help='This Transactions Type is used as default if there is more then one for a given situation')
    conciliable = fields.Boolean('Conciliable')
#    requires_authorization = fields.Boolean('requires_authorization ')
#    allows_scheduled_payments = fields.Boolean('allows_scheduled_payments')
    confirmation_message = fields.Text('Confirmation Message')
    max_amount_per_day = fields.Float('Max amount per day to transfer')
#    reserve_total_on_sched = fields.Boolean('reserve_total_on_sched')
#    allow_cancel_sched = fields.Boolean('allow_cancel_sched')
#    allow_block_sched = fields.Boolean('allow_block_sched')
#    show_sched_to_dest = fields.Boolean('show_sched_to_dest')
    requires_feedback = fields.Boolean('Requires Feedback')
    feedback_enabled_since = fields.Date('Feedback expected since')
    feedback_expiration_time_number = fields.Integer('Feedback expected in days')
    feedback_reply_expiration_time_number = fields.Integer('Feedback reply expiration in days')
    default_feedback_comments = fields.Text('Default feedback comment')
    # TODO should be related to: Exchange Rating API exchange_rating.type
    default_feedback_level = fields.Integer('Default feedback level')
    feedback_account_id = fields.Many2one(
        'exchange.config.accounts', 'Feedback account', required=False,
        help='Related account to transfer Rating points')
    is_fee = fields.Boolean('Is a fee transaction')
    feetype_id = fields.Many2one(
        'exchange.transaction.type', 'Transaction Type ID', required=False)
    feetype_ids = fields.One2many(
        'exchange.transaction.type', 'feetype_id', 'Included Transactions', required=False)
    fee_type = fields.Selection(
            [
                ('fix', 'Fix Amount'),
                ('percent', 'Percentage'),
            ], 'Type of fee', readonly=False, required=False, track_visibility='onchange')
    fee = fields.Float(
        'Amount of Fee', required=False,
        help='Amount of Fee in currency or percentage')
    # Loan fields/process not yet clear?
    is_loan = fields.Boolean('Is a loan transaction',
            help='Is a loan/grant transaction type')
    """ TODO
    loan_contract_type_ids = fields.Many2one(
        'exchange.loan.contract.type',
        'Loan Contract Type', required=False,
        help='Related type of loan to this loan transaction')
    """
    loan_tr_type = fields.Selection(
            [
                ('grant', 'Grant'),
                ('init_fee', 'Initial fee'),
                ('expiration_fee', 'Expiration fee'),
                ('interest', 'Interest'),
                ('repayment', 'Repayment'),
            ], 'Loan Status', readonly=False, required=False, track_visibility='onchange')
    # Related fields (not stored in DB)
    type_prefix_from = fields.Many2one('exchange.account.type',
         'Prefix from', related='from_account_type_id.type_prefix',
         readonly=True)
    type_prefix_to = fields.Many2one('exchange.account.type',
         'Prefix to', related='to_account_type_id.type_prefix',
         readonly=True)


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
    _name = 'exchange.transaction.line'
    _description = 'Exchange Entries'
    _order = 'id desc'

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

    name = fields.Char('Name', default=datetime.now(), required=True, copy=False)
    ref = fields.Char('Reference', copy=False)
    transfer_type = fields.Selection([
        ('transfer','Transfer'),
        ('invoice','Invoice'),
        ('inv_confirm','Invoice Confirm'),
        ('transfer_to_confirm','Transfer to Confirm'),
        ('refund','Refund'),
        ('info','Info/Message')],
        'Transfer Type', required=True, readonly=False,
        track_visibility='onchange', copy=False,
        help='Bla Bla status.')
    type_id = fields.Many2one(
        'exchange.transaction.type', 'Transactions Type', required=False)
    transfer_from_id = fields.Many2one(
        'exchange.accounts', 'Transfer From',
        required=True)
    transfer_to_id = fields.Many2one(
        'exchange.accounts', 'Transfer To',
        required=True, default=get_field)
    transfer_from_hash = fields.Text(
        'Hash From', required=False)
    transfer_to_hash = fields.Text(
        'Hash To', required=False)
    content = fields.Text(
        'Message', required=False,
        help='Note or Message in case of info transfer.')
    transaction_id = fields.Many2one('exchange.transaction',
        'Related Transaction',
        #   transfer_type={'send':[('readonly',True)]},
        copy=True)
    to_check = fields.Boolean('To Review',
        help='Check this box if you are unsure of that that entry and if you want to note it as \'to be reviewed\' by an accounting expert.')
    amount_from = fields.Float('Amount from', required=False, default=5.0)
#  TODO amount_from = fields.Float('Amount from', required=False, default='exchange.transaction.amount_from')
    amount_to = fields.Float('Amount to', transfer_type={'transfer':[('required=True')]})
    date = fields.Date('Date',  default=datetime.now(), required=True, readonly=True, select=True)

    # Related fields (not stored in DB)
    account_from = fields.Many2one('exchange.transaction',
         'Account from', related='transaction_id.account_from_id',
         readonly=True)
    account_to = fields.Many2one('exchange.transaction',
         'Account to', related='transaction_id.account_to_id',
         readonly=True)


class ExchangeTransactions(models.Model):
    """
    Main object used for the workflow of transferring values, invoices and messages , from sender_account to receiver_account    It has his own workflow, from draft to paid and can be refund.

    """

    _name = 'exchange.transaction'
    _description = 'Exchange Transactions'
    _inherit = ['mail.thread']
    _order = 'emission_date'
    #   Track the status of the transaction to mail.thread
    #   _track = 'state', 'account_wallet.mt_transaction_state': lambda self,
    #           obj, ctx=None: obj.already_published,

    name = fields.Char(
        'Number', size=30, required=True)
    # TODO       default=tr_number_calc('type_id'))
    account_from_id = fields.Many2one(
        'exchange.accounts', 'Account From', required=True, state={'draft': [('readonly', False)]},
        track_visibility='onchange')
    account_to_id = fields.Many2one(
        'exchange.accounts', 'Account To', required=True, state={'draft': [('readonly', False)]},
        track_visibility='onchange')
    type_id = fields.Many2one(
        'exchange.transaction.type', 'Transactions Type', state={'draft': [('readonly', False)]}, required=True)
    line_ids = fields.One2many(
        'exchange.transaction.line', 'transaction_id', 'Transfer Lines', required=False)
    emission_date = fields.Datetime(
        'Emission Date', required=True, readonly=True, default=datetime.now().strftime("%Y-%m-%d"))
    transaction_date = fields.Datetime(
        'Transaction Date', required=False)
    emission_from = fields.Many2one(
        'res.partner', 'Issued from',
        default=lambda self: self.env['exchange.model'].user_partner)
    amount_from = fields.Float(
        'Amount from Sender', state={'draft': [('readonly', False)]}, required=True)
    # TODO: should be computed out of exchange rates in res.currency
    amount_to = fields.Float(
        'Amount to Receiver', required=True, state={'draft': [('readonly', False)]},
        track_visibility='onchange')

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('sent', '⌛Sent'),
            ('invoiced', '⌛Invoiced'),
            ('paid', 'Paid'),
            ('refunded', 'Refunded'),
            ('denied', 'Denied'),
            ('canceled', 'Cancelled'),
        ], 'Status', readonly=False, default='draft', required=True, track_visibility='onchange')

    is_fee = fields.Boolean(
        'Transaction has fees', state={'draft': [('readonly', False)]})
    is_invoice = fields.Boolean(
        'Invoice Transaction', track_visibility='onchange', state={'draft': [('readonly', False)]})

    is_loan = fields.Boolean('Is a loan transaction', track_visibility='onchange')
    """
    loan_contract_id = fields.Many2one(
        'exchange.loan.contract', 'Related Loan contract', state={'draft': [('readonly', False)]}, required=False)
    """
    # Related fields (not stored in DB)
    sender_id = fields.Many2one('res.partner',
                                'Sending Partner', related='account_from_id.partner_id',
                                readonly=True)
    receiver_id = fields.Many2one('res.partner',
                                  'Receiving Partner', related='account_to_id.partner_id',
                                  readonly=True)
    currency_from = fields.Many2one('res.currency',
                                    'Currency from', related='account_from_id.currency_base',
                                    readonly=True)
    currency_to = fields.Many2one('res.currency',
                                  'Currency to', related='account_to_id.currency_base',
                                  readonly=True)
    exchange_rate_from = fields.Float(
        'Exchange rate Sender', related='account_from_id.exchange_rate',
        readonly=True, store=True)
    exchange_rate_to = fields.Float(
        'Exchange rate Receiver', related='account_to_id.exchange_rate',
        readonly=True, store=True)
    """
    ext_from = fields.Boolean(
        'From external Account', related='account_from_id.is_external',
        readonly=True, store=True)
    ext_to = fields.Boolean(
        'To external Account', related='account_to_id.is_external',
        readonly=True)
    """
    type_prefix_from = fields.Many2one('exchange.account.type',
                                       'Prefix from', related='type_id.type_prefix_from',
                                       readonly=True)
    type_prefix_to = fields.Many2one('exchange.account.type',
                                     'Prefix to', related='type_id.type_prefix_to',
                                     readonly=True)
    messaging_from = fields.Boolean(
        string='Messaging from', related='account_from_id.with_messaging',
        readonly=True)
    messaging_to = fields.Boolean(
        string='Messaging to', related='account_to_id.with_messaging',
        readonly=True)

    # TODO Computed fields (not stored in DB)
    user_role = fields.Char(
        'User role', store=False,
        compute='_get_user_role', track_visibility='onchange')