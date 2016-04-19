# -*- coding: utf-'8' "-*-"

import json
import logging

from openerp import models, fields, api
from openerp.tools.float_utils import float_compare
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class AccountTemplateConfig(models.Model):
    # Lines containing the general configuration of account templates
    _inherit = 'exchange.config.accounts'

    @api.onchange('exchange_provider_id')
    def _get_template_name(self):
        self.image = self.exchange_provider_id.image

    @api.multi
    def _compute_external(self):
        if self.exchange_provider_id.environment == "internal":
            return False
        else:
            return True

    exchange_provider_id = fields.Many2one('exchange.provider', 'Exchange Provider',
                                           help='Related Transaction engine internal or external')
    is_external = fields.Boolean(compute='_compute_external', string='External Account')
    """
    config_id = fields.Many2one(
        'exchange.config.settings', 'Config ID', required=False)
    """
    initcredit_type = fields.Many2one('exchange.transaction.type', 'Initial credit transaction type')
