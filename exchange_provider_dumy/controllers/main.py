# -*- coding: utf-8 -*-
# unchanged code from payment_sips
import json
import logging
import werkzeug

from openerp import http
from openerp.http import request

_logger = logging.getLogger(__name__)


class DumyController(http.Controller):
    _notify_url = '/exchange_provider/dumy/ipn/'
    _return_url = '/exchange_provider/dumy/dpn/'


    def _get_return_url(self, **post):
        # Extract the return URL from the data coming from dumy.
        return_url = post.pop('return_url', '')
        if not return_url:
            tx_obj = request.registry['exchange.transaction']
            data = tx_obj._dumy_data_to_object(post.get('Data'))
            custom = json.loads(data.pop('returnContext', False) or '{}')
            return_url = custom.get('return_url', '/')
        return return_url

    def dumy_validate_data(self, **post):
        res = False
        env = request.env
        tx_obj = env['exchange.transaction']
        provider_obj = env['exchange.provider']

        dumy = provider_obj.search([('provider', '=', 'dumy')], limit=1)

        security = dumy._dumy_generate_shasign(post)
        if security == post['Seal']:
            _logger.debug('Dumy: validated data')
            res = tx_obj.sudo().form_feedback(post, 'dumy')
        else:
            _logger.warning('Dumy: data are corrupted')
        return res

    @http.route([
        '/payment/dumy/ipn/'],
        type='http', auth='none', methods=['POST'], csrf=False)
    def dumy_ipn(self, **post):
        # Dumy IPN.
        self.dumy_validate_data(**post)
        return ''

    @http.route([
        '/payment/dumy/dpn'], type='http', auth="none", methods=['POST'], csrf=False)
    def dumy_dpn(self, **post):
        # Dumy DPN
        return_url = self._get_return_url(**post)
        self.dumy_validate_data(**post)
        return werkzeug.utils.redirect(return_url)



