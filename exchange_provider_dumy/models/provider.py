# -*- coding: utf-'8' "-*-"

import json
import logging
from hashlib import sha256
import urlparse
import unicodedata

from odoo import api, fields, models, exceptions
from odoo.tools.float_utils import float_compare
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError
from ..controllers.main import DumyController

_logger = logging.getLogger(__name__)

# Supported Currencies
CURRENCY_CODES = {
    'EUR': '001',
    'USD': '001',
    'CHF': '003',
    'DOO': '004',
    'BTC': '005',
    'ETH': '006',
}


class ProviderDumy(models.Model):
    _inherit = 'exchange.provider'
    # credentials Fields
    dumy_id = fields.Char('Dumy API User ID', required_if_provider='dumy')
    dumy_secret = fields.Char('Dumy Secret', size=64, required_if_provider='dumy')
    # Fees, (are only relevant in case of fees that are not included in the transaction logic)
    fees_active = fields.Boolean('Add Extra Fees')
    fees_dom_fixed = fields.Float('Fixed domestic fees')
    fees_dom_var = fields.Float('Variable domestic fees (in percents)')
    fees_int_fixed = fields.Float('Fixed international fees')
    fees_int_var = fields.Float('Variable international fees (in percents)')

    # Methods
    def _get_dumy_urls(self, environment):
        # Dumy URLS
        url = {
            'prod': 'https://exchange.com/ExInit',
            'test': 'https://test.exchange.com/ExInit', }

        return {'dumy_form_url': url.get(environment, url['test']), }

    @api.model
    def _get_providers(self):
        providers = super(ProviderDumy, self)._get_providers()
        providers.append(['dumy', 'Dumy'])
        return providers

    @api.one  # Here the code for testing the connection has to be ad
    def _act_provider_test_dumy(self):
        test = True
        if test is True:
            raise exceptions.Warning('This is not a valid connection (Dumy Module)!')
        return "test"

    @api.one  # Here the code for getting the balance has to be ad
    def _get_provider_balance_dumy(self):
        test = True
        if test is True:
            raise exceptions.Warning('This is not a valid balance (Dumy Module)!')
        return float(50.0)

    """

    def _dumy_generate_shasign(self, values):
        # Generate the shasign for incoming or outgoing communications.
        # :param dict values: transaction values
        # :return string: shasign

        if self.provider != 'dumy':
            #  raise Exception(_('Incorrect payment exchange provider'))
            raise ValidationError(_('Incorrect payment exchange provider'))
        data = values['Data']

        # Test key provided by ?
        key = u'002001000000001_KEY1'

        if self.environment == 'prod':
            key = getattr(self, 'dumy_secret')

        shasign = sha256(data + key)
        return shasign.hexdigest()

    @api.multi
    def dumy_form_generate_values(self, values):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        currency = self.env['res.currency'].sudo().browse(values['currency_id'])
        currency_code = CURRENCY_CODES.get(currency.name, False)
        if not currency_code:
            raise Exception(_('Currency not supported by Dumy'))
            # raise ValidationError(_('Currency not supported by Dumy'))
        amount = int(values['amount'] * 100)
        if self.environment == 'prod':
            # For production environment, key version 2 is required
            dumy_id = getattr(self, 'dumy_id')
            key_version = '2'
        else:
            # Test key provided by Dumy
            dumy_id = '0020010000002201'
            key_version = '1'

        dumy_tx_values = dict(values)
        dumy_tx_values.update({
            'Data': u'amount=%s|' % amount +
                    u'currencyCode=%s|' % currency_code +
                    u'dumyId=%s|' % dumy_id +
                    u'normalReturnUrl=%s|' % urlparse.urljoin(base_url, DumyController._return_url) +
                    u'automaticResponseUrl=%s|' % urlparse.urljoin(base_url, DumyController._return_url) +
                    u'transactionReference=%s|' % values['reference'] +
                    u'statementReference=%s|' % values['reference'] +
                    u'keyVersion=%s' % key_version,
            'InterfaceVersion': 'HP_2.3',
        })

        return_context = {}
        if dumy_tx_values.get('return_url'):
            return_context[u'return_url'] = u'%s' % dumy_tx_values.pop('return_url')
        return_context[u'reference'] = u'%s' % dumy_tx_values['reference']
        dumy_tx_values['Data'] += u'|returnContext=%s' % (json.dumps(return_context))

        shasign = self._dumy_generate_shasign(dumy_tx_values)
        dumy_tx_values['Seal'] = shasign
        return dumy_tx_values

    @api.multi
    def dumy_get_form_action_url(self):
        self.ensure_one()
        return self._get_dumy_urls(self.environment)['dumy_form_url']

    """

