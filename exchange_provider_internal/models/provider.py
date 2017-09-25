# -*- coding: utf-'8' "-*-"

import json
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProviderInternal(models.Model):
    _inherit = 'exchange.provider'
    # no special fields

    # Methods
    @api.model
    def _get_providers(self):
        providers = super(ProviderInternal, self)._get_providers()
        providers.append(['internal', 'Internal Transaction Engine'])
        return providers

