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
    _name = 'exchange.config.settings'
    _description = 'Exchange configuration'

    _inherit = 'res.config.settings'


class ResCurrency(models.Model):
    """
    Add a boolean in currency to identify currency usable in wallet/exchange
    """
    _inherit = 'res.currency'

    exchange_currency = fields.Boolean('Exchange currency?', readonly=False)

