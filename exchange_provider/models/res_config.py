# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber, Yannick Buron>
# based on account_wallet by Yannick Buron, Copyright Yannick Buron
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging
import openerp
from openerp import models, fields, api
from openerp.tools import image_get_resized_images, image_resize_image_big
_logger = logging.getLogger(__name__)


class ExchangeConfigSettings(models.TransientModel):

    """
    Exchange settings which will be used to contain all configuration
    """
    _inherit = 'exchange.config.settings'

    exchange_provider_id = fields.Many2one('exchange.provider', 'Exchange Provider',
                                           help='Related Transaction engine internal or external')

    exch_code = fields.Char(
        'Exchange Code', related='exchange_provider_id.exch_code',
        help="Unique Exchange Code (EC)"
             "First part of the 20 digits Account Code CC BBBB"
             "CC country code -> DE Germany"
             "BBBB Exchange code")

    # Related fields
    is_external = fields.Boolean(string='External Account', related='exchange_provider_id.is_external')
    display_balance = fields.Boolean('Everyone can see balances?',
                                     related='exchange_provider_id.display_balance')
    use_account_numbers = fields.Boolean(
        'Use of Account Numbering System', related='exchange_provider_id.use_account_numbers',
        help="Use of the 20 digits Account Numbering Code 'CC BBBB DDDDDDDD XXXX-KK'")
    email_sysadmin = fields.Char('Sysadmin mail address', related='exchange_provider_id.email_sysadmin')
    # account_conf_ids = fields.One2many('Accounts templates', related='exchange_provider_id.account_conf_ids')







