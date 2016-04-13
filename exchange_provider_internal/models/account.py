# -*- coding: utf-'8' "-*-"

import json
import logging

from openerp import models, fields, api
from openerp.tools.float_utils import float_compare
from openerp.tools.translate import _
from openerp.addons.base_exchange.models.exchange_provider import ValidationError

_logger = logging.getLogger(__name__)


class ProviderAccount(models.Model):
    #    List of Accounts for members and the system
    _name = 'exchange.provider.internal'
    _description = 'Exchange Provider Accounts Internal'
    _order = 'template_id,partner_id,name'

    @api.onchange('template_id')
    def _get_creditlimit(self):
        print self
        limitout = 9.0
        # template_id.limit_positive_value
        limitout = self.env['exchange.config.accounts'].browse(self._context.get('limit_positive_value'))
        print limitout
        self.limit_positive_value = limitout

    name = fields.Char('Account Name', size=64, required=True)
    provider = fields.Many2one(related='template_id.provider', string='Provider', required=False)
    # TODO should be computed field out of 'number_prefix' & 'GeneratedNumber' & 'currency_id'
    number = fields.Char(
        'Account Number', required=True,
        size=16, help='Number of the Account', default='CH-XX-123456')
    key = fields.Text(
        'Key', readonly=True,
         help="Account key for the use in outside DB/ledger")
    desc = fields.Text('Description')
    template_id = fields.Many2one(
        'exchange.config.accounts', 'Account Template',
        track_visibility='onchange', required=True)
    partner_id = fields.Many2one(
        'res.partner', 'Partner')
    limit_negative = fields.Boolean('Limit - ?')
    limit_negative_value = fields.Float(
        'Credit Limit -', default=0.0)
    limit_positive = fields.Boolean('Limit + ?')
    limit_positive_value = fields.Float(
        'Account Limit +')

    state = fields.Selection([
        ('open', 'Open'),
        ('blocked', 'Blocked'),
        ('closed', 'Closed'),
        ], 'Account Status', readonly=False,
        required=True, default='open', track_visibility='onchange',
        help="Status of Account"
             "Blocked, for temporary blocking transactions")
    # Related fields (stored in DB)
    type_prefix = fields.Many2one('exchange.account.type',
        'Account Type Prefix', related='template_id.type_prefix',
         readonly=True, store=True)
    external_db = fields.Boolean(
        'External DB', related='template_id.external_db',
         readonly=True, store=True,
         help="Account is performing transactions on an a outside DB/ledger")
    default_account = fields.Boolean(
        'Default account', related='template_id.default_account',
         readonly=True, store=True)
    currency_base = fields.Many2one('res.currency',
        'Currency', related='template_id.currency_id',
         readonly=True)
    exchange_rate = fields.Float(
        'Exchange Rate', related='template_id.exchange_rate', readonly=True)
    user_id = fields.One2many('res.users',
        'User ID', related='partner_id.user_ids', readonly=True)
    with_messaging = fields.Boolean(
        string='Messaging', related='template_id.with_messaging',
        readonly=True)
    image = fields.Binary("Image", related='template_id.image')
    image_medium = fields.Binary("Medium-sized image",
                                 related='template_id.image_medium')
    image_small = fields.Binary("Small-sized image",
                                related='template_id.image_small')
    # Computed fields
    # Next 2 fields are TODO
    available = fields.Float(
        'Available', store=False,
        compute='_get_available_amount')
    balance = fields.Float(
        'Account Balance', store=False,
        compute='_get_balance')
    reserved = fields.Float('Reserved')
    # ref = fields.Reference('Reference', selection=openerp.addons.base.res.res_request.referencable_models)

    @api.one
    def do_account_deblock(self):
        self.state = 'open'

    @api.one
    def do_account_block(self):
        self.state = 'blocked'

    @api.one
    def do_account_close(self):
        self.state = 'closed'

    @api.one
    @api.depends('balance', 'limit_negative_value')  # computed field available calculate
    def _get_available_amount(self):
        for record in self:
            record.available = self.balance - self.limit_negative_value

    @api.one # computed field balance calculate
    def _get_balance(self):

        self.balance = 100.0


#    @api.one
#    @api.constrains('account_type', 'partner_id', 'number')
#    def _check_application(self):
#        """
#        Check that the Account are single then other as user accounts
#        """
#        if self.account_type != user
#                self.account_type.id:
#            raise except_orm(_('Data error!'),
#                             _("Only user accounts can have more than one per type"))
#        else
#                self.partner_id.id:
#            raise except_orm(_('Data error!'),
#                             _("Only one user accounts per type"))


class TxDumy(models.Model):
    _inherit = 'payment.transaction'

    # dumy status
    _dumy_valid_tx_status = ['00']
    _dumy_wait_tx_status = ['90', '99']
    _dumy_refused_tx_status = ['05', '14', '34', '54', '75', '97']
    _dumy_error_tx_status = ['03', '12', '24', '25', '30', '40', '51', '63', '94']
    _dumy_pending_tx_status = ['60']
    _dumy_cancel_tx_status = ['17']

    # --------------------------------------------------
    # FORM RELATED METHODS
    # --------------------------------------------------
    def _dumy_data_to_object(self, data):
        res = {}
        for element in data.split('|'):
            element_split = element.split('=')
            res[element_split[0]] = element_split[1]
        return res

    @api.model
    def _dumy_form_get_tx_from_data(self, data):
        """ Given a data dict coming from dumy, verify it and find the related
        transaction record. """

        data = self._dumy_data_to_object(data.get('Data'))
        reference = data.get('transactionReference')

        if not reference:
            custom = json.loads(data.pop('returnContext', False) or '{}')
            reference = custom.get('reference')

        payment_tx = self.search([('reference', '=', reference)])
        if not payment_tx or len(payment_tx) > 1:
            error_msg = _('Dumy: received data for reference %s') % reference
            if not payment_tx:
                error_msg += _('; no order found')
            else:
                error_msg += _('; multiple order found')
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        return payment_tx

    @api.model
    def _dumy_form_get_invalid_parameters(self, tx, data):
        invalid_parameters = []

        data = self._dumy_data_to_object(data.get('Data'))

        # TODO: txn_id: should be false at draft, set afterwards, and verified with txn details
        if tx.exchange_reference and data.get('transactionReference') != tx.exchange_reference:
            invalid_parameters.append(('transactionReference', data.get('transactionReference'), tx.exchange_reference))
        # check what is bought
        if float_compare(float(data.get('amount', '0.0')) / 100, tx.amount, 2) != 0:
            invalid_parameters.append(('amount', data.get('amount'), '%.2f' % tx.amount))
        if tx.partner_reference and data.get('customerId') != tx.partner_reference:
            invalid_parameters.append(('customerId', data.get('customerId'), tx.partner_reference))

        return invalid_parameters

    @api.model
    def _dumy_form_validate(self, tx, data):
        data = self._dumy_data_to_object(data.get('Data'))
        status = data.get('responseCode')
        data = {
            'exchange_reference': data.get('transactionReference'),
            'partner_reference': data.get('customerId'),
            'date_validate': data.get('transactionDateTime',
                                      fields.Datetime.now())
        }
        res = False
        if status in self._dumy_valid_tx_status:
            msg = 'Payment for tx ref: %s, got response [%s], set as done.' % \
                  (tx.reference, status)
            _logger.info(msg)
            data.update(state='done', state_message=msg)
            res = True
        elif status in self._dumy_error_tx_status:
            msg = 'Payment for tx ref: %s, got response [%s], set as ' \
                  'error.' % (tx.reference, status)
            data.update(state='error', state_message=msg)
        elif status in self._dumy_wait_tx_status:
            msg = 'Received wait status for payment ref: %s, got response ' \
                  '[%s], set as error.' % (tx.reference, status)
            data.update(state='error', state_message=msg)
        elif status in self._dumy_refused_tx_status:
            msg = 'Received refused status for payment ref: %s, got response' \
                  ' [%s], set as error.' % (tx.reference, status)
            data.update(state='error', state_message=msg)
        elif status in self._dumy_pending_tx_status:
            msg = 'Payment ref: %s, got response [%s] set as pending.' \
                  % (tx.reference, status)
            data.update(state='pending', state_message=msg)
        elif status in self._dumy_cancel_tx_status:
            msg = 'Received notification for payment ref: %s, got response ' \
                  '[%s], set as cancel.' % (tx.reference, status)
            data.update(state='cancel', state_message=msg)
        else:
            msg = 'Received unrecognized status for payment ref: %s, got ' \
                  'response [%s], set as error.' % (tx.reference, status)
            data.update(state='error', state_message=msg)

        _logger.info(msg)
        tx.write(data)
        return res
