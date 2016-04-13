# -*- coding: utf-'8' "-*-"

import json
import logging
from hashlib import sha256
import urlparse
import unicodedata

from openerp import models, fields, api
from openerp.tools.float_utils import float_compare
from openerp.tools.translate import _
from openerp.addons.base_exchange.models.exchange_provider import ValidationError
from exchange_provider_dumy.controllers.main import DumyController

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
    # Fields
    ip = fields.Char('IP', size=64, required=True)
    port = fields.Integer('port', required=True)
    db_hash = fields.Char('Hash of the DB')
    login = fields.Char('Loginname to external DB')
    pw = fields.Char('Password to external DB')
    use_keys = fields.Boolean(
        'Using keys?',
        help='Using keys instead of login/password?')
    private_key = fields.Text(
        'Private Key', required=True,
        default='XXXX')
    public_key = fields.Text(
        'Public Key', required=True,
        default='XXXX')
    goclouder = fields.Boolean(
        'Is a Goclouder Docker container?',
        help='Is a Goclouder Docker container?')
#    clouder_container_ids = fields.One2many('clouder.container',
#                                            'container_id', 'Ports')
    merchant_id = fields.Char('SIPS API User Password',
                                   required_if_provider='sips')
    sips_secret = fields.Char('SIPS Secret', size=64, required_if_provider='sips')

    # Methods
    def _get_dumy_urls(self, environment):
        """ Dumy URLS """
        url = {
            'prod': 'https://exchange.com/ExInit',
            'test': 'https://test.exchange.com/ExInit',}

        return {'dumy_form_url': url.get(environment, url['test']),}

    @api.model
    def _get_providers(self):
        providers = super(ProviderDumy, self)._get_providers()
        providers.append(['dumy', 'Dumy'])
        return providers

    def _dumy_generate_shasign(self, values):
        """ Generate the shasign for incoming or outgoing communications.
        :param dict values: transaction values
        :return string: shasign
        """
        if self.provider != 'dumy':
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
            raise ValidationError(_('Currency not supported by Dumy'))
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