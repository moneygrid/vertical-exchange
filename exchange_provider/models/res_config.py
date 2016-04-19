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

    is_external = fields.Boolean(compute='_compute_external', string='External Account')
    """
    account_ids = fields.One2many(
        'exchange.config.accounts', 'config_id', 'Accounts templates')
    """
    # TODO may raise conflicts with exchange rates in accounting system



