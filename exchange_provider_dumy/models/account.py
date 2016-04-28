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

    account_id_dumy = fields.Many2one('exchange.account.provider.dumy', 'Account link to Provider',
                                      track_visibility='onchange', required=True)


class ProviderAccount(models.Model):
    #    List of Accounts for members and the system
    _name = 'exchange.account.provider.dumy'
    _description = 'Exchange Provider Accounts Dumy'
    _order = 'template_id,name'

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

    @api.one  # computed field balance calculate
    def _get_balance(self):
        self.balance = 1900.0


    """
class TxDumy(models.Model):
    _inherit = 'exchange.transaction'

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
        # Given a data dict coming from dumy, verify it and find the related
        # transaction record.

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
    """