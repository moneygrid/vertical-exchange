# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


import openerp
from openerp import models, fields, api, exceptions
from openerp.tools import image_get_resized_images, image_resize_image_big
import logging
_logger = logging.getLogger(__name__)


class ValidationError(ValueError):
    """ Used for value error when validating transaction data coming from Exchange Providers. """
    pass

    """
class ExchangeProviderModel(models.Model):
    """
    # Model allocation for the Exchange Providers
    """
    _name = 'exchange.provider.model'
    _description = 'Exchange Provider Models'
    _order = 'name'

    name = fields.Char('Name', size=64, required=True)
    account_model_id = fields.Many2one('ir.model', string='Account Model', required=False)
    transaction_model_id = fields.Many2one('ir.model', string='Transaction Model', required=False)
    description = fields.Text('Description')
    """


class ExchangeProviderCurrencies(models.Model):
    """
    Available Currencies for the Exchange Providers
    """
    _name = 'exchange.provider.currency'
    _description = 'Exchange Provider Currencies'
    _order = 'sequence'

    name = fields.Char('Name', size=64, required=True)
    sequence = fields.Integer('Sequence', help="Determine the display order")
    provider_id = fields.Many2one('exchange.provider', string='Provider', required=False)
    # provider = fields.Selection(_provider_selection, string='Provider', required=True)
    description = fields.Text('Description')
    currency_id = fields.Many2one('res.currency', 'Currency', required=True)
    currency_symbol = fields.Char('Symbol', related='currency_id.symbol')
    currency_rate = fields.Float('Rate', related='currency_id.rate')


class ExchangeProvider(models.Model):
    """ Base Model for Transaction engines or external DB's
    Exchange Provider Model. Each specific Exchange Provider can extend the model by adding
    its own fields, using the Exchange Provider_name as a prefix for the new fields.
    Using the required_if_provider='<name>' attribute on fields it is possible
    to have required fields that depend on a specific Exchange Provider.

    Methods that should be added in an Exchange Provider-specific implementation:

     - ``<name>_form_generate_values(self, values)
        reference, amount, currency,
       partner_id=False, partner_values=None, tx_custom_values=None, context=None)``:
       method that generates the values used to render the form button template.
     - ``<name>_get_form_action_url(self,):``: method
       that returns the url of the button form. It is used
       to post some data to the Exchange Provider.
     - ``<name>_compute_fees(self, amount, currency_id, country_id)``:
       computed the fees of the Exchange Provider, using generic fields
       defined on the Exchange Provider model (see fields definition).

    Each Exchange Provider should also define controllers to handle communication between
    Odoo and the Exchange Provider. It generally consists in return urls given to the
    payment form and that the Exchange Provider uses to send the customer back after the
    transaction, with transaction details given as a POST request.
    """

    _name = 'exchange.provider'
    _description = 'Exchange Provider'
    _order = 'sequence'

    @api.model  # collects selection items from provider modules
    def _get_providers(self):
        return []

    # indirection to ease inheritance
    _provider_selection = lambda self, *args, **kwargs: self._get_providers(*args, **kwargs)

    name = fields.Char('Name', size=64, required=True)
    sequence = fields.Integer('Sequence', help="Determine the display order")
    provider = fields.Selection(_provider_selection, string='Provider', required=True)
    # TODO provider_model = fields.Many2one('exchange.provider.model', string='Provider Model', required=False)
    ref_provider = fields.Reference(
        [('exchange.provider.internal', 'Internal'), ('exchange.provider.dumy', 'Dumy')],
        'Accounts PR')
   # balance = fields.Float(
   #    'Balance Pr', related='ref_provider.balance', readonly=True)
    account_conf_ids = fields.One2many('exchange.config.accounts', 'exchange_provider_id', string='Account Templates',
                                       required=False)
    connection = fields.Selection(
        [('none', 'No connection'),
         ('single', 'Singlepoint'),
         ('multiuser', 'Multiple Users'),
         ('multisys', 'Multiple Accounts')],
        string='Connection Type', required=True,
        help="Defines how the provider connected to the Exchange framework."
             "- Single-point connection. Eg. a Clearing account"
             "- Multiple Users connection -> Eg. normal usecase with ext. transaction engine"
             "- Multiple Accounts connection -> One Admin can manage all account")
    singlepoint = fields.Boolean(string='Singlepoint Provider', readonly=True,  # TODO
                                 help="if checked the provider is serving only a single"
                                      " point connection. Eg. a Clearing account")
    environment = fields.Selection(
        [('internal', 'Internal'),
         ('test', 'External Test'),
         ('prod', 'External Production')],
        string='Environment', required=True)
    test_url = fields.Char('Test URL', required=False)
    test_login = fields.Char('Test Login', size=64, required=False)
    test_secret = fields.Char('Test secret', size=128, required=False)
    asset_class = fields.Char('Asset Class', size=64, required=False)
    active = fields.Boolean('Active?', default=False)
    partner_id = fields.Many2one('res.partner',  string='Related Partner')
    currency_ids = fields.One2many('exchange.provider.currency', 'provider_id',  readonly=True,
                                   string='Provided Currencies')
    currency_id = fields.Many2one('exchange.provider.currency', 'Currency', required=False,
                                  help="Currency used for this Provider Configuration"
                                       "(only by the module provided currencies are available!)")
    view_template_id = fields.Many2one('ir.ui.view', 'Form Button Template', required=False)
    """
    registration_view_template_id = fields.Many2one('ir.ui.view', 'Form Template',
                                                     domain=[('type', '=', 'qweb')],
                                                     help="Template for method registration")
    """
    description = fields.Text('Description')
    image = fields.Binary("Image", attachment=True,
                          help="This field holds the image used for this Exchange Provider, limited to 1024x1024px")
    image_medium = fields.Binary("Medium-sized image",
                                 compute='_compute_images', inverse='_inverse_image_medium', store=True,
                                 attachment=True,
                                 help="Medium-sized image of this Exchange Provider. It is automatically " \
                                      "resized as a 128x128px image, with aspect ratio preserved. " \
                                      "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image",
                                compute='_compute_images', inverse='_inverse_image_small', store=True,
                                attachment=True,
                                help="Small-sized image of this Exchange Provider. It is automatically " \
                                     "resized as a 64x64px image, with aspect ratio preserved. " \
                                     "Use this field anywhere a small image is required.")
    pre_msg = fields.Html('Help Message', translate=True,
                          help='Message displayed to explain and help the payment process.')
    post_msg = fields.Html('Thanks Message', help='Message displayed after having done the payment process.')
    pending_msg = fields.Html('Pending Message', translate=True,
                        help='Message displayed, if order is in pending state after having done the payment process.')
    done_msg = fields.Html('Done Message', translate=True,
                        help='Message displayed, if order is done successfully after having done the payment process.')
    cancel_msg = fields.Html('Cancel Message', translate=True,
                             help='Message displayed, if order is cancel during the payment process.')
    error_msg = fields.Html('Error Message', translate=True,
                            help='Message displayed, if error is occur during the payment process.')
    # Fees
    fees_active = fields.Boolean('Add Extra Fees')
    fees_dom_fixed = fields.Float('Fixed domestic fees')
    fees_dom_var = fields.Float('Variable domestic fees (in percents)')
    fees_int_fixed = fields.Float('Fixed international fees')
    fees_int_var = fields.Float('Variable international fees (in percents)')
    balance_test = fields.Float('Balance')

    @api.depends('image')
    def _compute_images(self):
        for rec in self:
            rec.image_medium = openerp.tools.image_resize_image_medium(rec.image)
            rec.image_small = openerp.tools.image_resize_image_small(rec.image)

    @api.one  # Action connection test via the provider models
    def act_provider_test(self):
        sub_function = "_act_provider_test_" + str(self.provider)
        call_test = getattr(self, sub_function)
        result = call_test()
        # function = self.sub_function2()
        print "function conn", sub_function, call_test, result

    @api.one  # get provider_balance from the provider models
    def act_provider_get_balance(self):
        sub_function = "_get_provider_balance_" + str(self.provider)
        call_balance = getattr(self, sub_function)
        result = call_balance()
        print "function_balance", sub_function, call_balance, result
        self.balance_test = result

