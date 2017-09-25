# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber, Yannick Buron>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from odoo.tools import image
# from odoo.exceptions import UserError, ValidationError
# import odoo.addons.decimal_precision as dp

#  from . import exchange.model


class ExchangeAccounts(models.Model):
    #    List of Accounts for members and the system
    _name = 'exchange.accounts'
    _description = 'Exchange Accounts'
    _order = 'template_id,partner_id,name'

    @api.onchange('template_id')
    def _get_template_name(self):
        self.name = self.template_id.name

    @api.onchange('template_id')
    def _get_credit_limits(self):
        self.limit_negative = self.template_id.limit_negative
        self.limit_negative_value = self.template_id.limit_negative_value
        self.limit_positive = self.template_id.limit_positive
        self.limit_positive_value = self.template_id.limit_positive_value

    @api.multi  # get partner_id from the res_users model
    def _compute_partner_id(self):
        for record in self:
            record.partner_id_id = record.partner_id.id

    @api.multi  # get partner_id from the res_users model
    def _compute_partner_id_cur(self):
        for record in self:
            record.partner_id_current = self.env.user.partner_id.id
            return self.env.user.partner_id.id

    @api.multi  # TODO   # get partner_id from the res_users model
    def _compute_partner_is_current(self):
        for record in self:
            if record.partner_id.id == self.env.user.partner_id.id:
                record.partner_is_current = True
                return True
            else:
                record.partner_is_current = False
                return False

    @api.onchange('acc_number')
    @api.multi  # get token from hash function of the account number
    def _compute_token(self):
        self.ensure_one()
        token = str(hash(self.acc_number))
        return token

    """
    @api.multi  # TODO   # get balance from the provider models
    def _compute_balance_mod(self):
        sub_function = "_act_provider_test_" + str(self.exchange_provider_module)
        call_test = getattr(self, sub_function)
        result = call_test()
        # function = self.sub_function2()
        print "function balance", sub_function, call_test, result
    """

    name = fields.Char('Account Name', translate=True, size=64, required=True)
    # TODO should be computed field out of 'number_prefix' & 'GeneratedNumber' & 'currency_id'
    acc_number = fields.Char(
        'Account Number', required=True,
        size=16, help='Number of the Account', default='CH-XX-123456')
    token = fields.Text(compute=_compute_token, string='Key or token', store=True,
                        readonly=True, help="Account token for the use in outside DB/ledger")
    color = fields.Integer('Color Index')
    sequence = fields.Integer('Sequence')
    locked = fields.Selection([
        ('open', 'Open'),
        ('ingoing', 'Ingoing'),
        ('outgoing', 'Outgoing'),
        ('al', 'All'),
        ], 'Account Lock', readonly=False,
        required=True, default='open', track_visibility='onchange',
        help="State of of Account Lock"
             "Every transaction locks Blocked the Account for a certain time (max 10sec)")
    state = fields.Selection([
        ('open', 'Open'),
        ('blocked', 'Blocked'),
        ('closed', 'Closed'),
        ], 'Account Status', readonly=False,
        required=True, default='open', track_visibility='onchange',
        help="Status of Account"
             "Blocked, for temporary blocking transactions")
    template_id = fields.Many2one(
        'exchange.config.accounts', 'Account Template', track_visibility='onchange', required=True)
    partner_id = fields.Many2one('res.partner', 'Account Owner')
    partner_id_id = fields.Integer(compute=_compute_partner_id, String='Partner ID')
    partner_id_current = fields.Integer(compute=_compute_partner_id_cur, String='Current Partner')
    partner_is_current = fields.Boolean(compute=_compute_partner_is_current, String='Is Current Partner')
    # user_id = fields.One2many('res.users', 'User ID', related='partner_id.user_ids', readonly=True)
    # Referenced Fields
    # ref = fields.Reference('Reference', selection=openerp.addons.base.res.res_request.referencable_models)
    """
     refers_to = fields.Reference(
        [('res.user', 'User'), ('res.partner', 'Partner')],
        'Refers to')
    """

    # Related fields (stored in DB)
    type_prefix = fields.Many2one('exchange.account.type',
        'Account Type Prefix', related='template_id.type_prefix', readonly=True, store=True)
    default_account = fields.Boolean(
        'Default account', related='template_id.default_account',
         readonly=True, store=True)
    currency_base = fields.Many2one('res.currency',
        'Currency', related='template_id.currency_id',
         readonly=True)
    exchange_rate = fields.Float(
        'Exchange Rate', related='template_id.exchange_rate', readonly=True)

    with_messaging = fields.Boolean(
        string='Messaging', related='template_id.with_messaging',
        readonly=True)
    image = fields.Binary("Image", related='template_id.image')
    image_medium = fields.Binary("Medium-sized image",
                                 related='template_id.image_medium')
    image_small = fields.Binary("Small-sized image",
                                related='template_id.image_small')
    desc = fields.Text('Description')

    @api.one
    def do_account_deblock(self):
        self.state = 'open'

    @api.one
    def do_account_block(self):
        self.state = 'blocked'

    @api.one
    def do_account_close(self):
        self.state = 'closed'


class AccountTypesType(models.Model):

    # Lines containing the list of accounts types
    _name = 'exchange.account.type'
    _description = 'Exchange Accounts Types list'

    name = fields.Char(
       'Account Type Key', required=True, size=2, translate=True, default="XX",
       help="Account key examples"
            "PD Private User Default account"
            "PU Private User sub-account"
            "BD Business User Default account"
            "BC Business User Credit account"
            "SY System account")
    account_name = fields.Char(
       'Account name', size=32, required=True,
       translate=True, default='XY User account',
       help="Name of the Account")
    account_desc = fields.Char(
       'Account Type Description',required=False,
       help='Description')

    _sql_constraints = [
        ('typename_unique', 'unique(name)',
        'We can only have one line per name'),
        ('account_name_unique', 'unique(account_name)',
        'We can only have one line per key'),
    ]


class AccountTemplateConfig(models.Model):
    # Lines containing the general configuration of account templates
    _name = 'exchange.config.accounts'
    _description = 'Exchange Account Type/Template configuration'

    name = fields.Char(
        'Account Name', required=True, size=40, translate=True,
        help='Name of the Account')

    account_type = fields.Selection([
        ('user', 'User account'),
        ('system', 'System account'),
        ('clearing', 'Clearing account'),
        ('rating', 'Rating account'),
        ], 'Account Type', readonly=False,
        required=True, default='user', track_visibility='onchange',
        help="Type of account /n"
             "User Account, belongs to a user"
             "System Account, belongs to the system or organisation"
             "Clearing Account, belongs to the system or organisation")

    type_prefix = fields.Many2one(
        'exchange.account.type', 'Account Number Prefix/Type', required=False, size=2,
        help="Prefix for Number of the Accounts"
             "in last part of the 21 digits Account Code")
    accounts_ids = fields.One2many(
        'exchange.accounts', 'template_id', 'Related accounts',
        help='Related accounts for transactions')

    hidden = fields.Boolean(
        'Hidden Account',
        help='Account is hidden to users')

    with_messaging = fields.Boolean(
        'Messaging',
        help='Account allows Messaging')

    default_account = fields.Boolean(
        'Default Account',
        default=False,
        help='This account will be used/attached for new users of the group')
    desc = fields.Text('Description')
    # TODO Filter on Many2one   about 'product.public.category' = Membership
    membership_type = fields.Many2one(
        'product.product', 'Type of membership', required=False,
        help='For this of membership the accounts will be used')

    currency_id = fields.Many2one(
        'res.currency', 'Currency',
        help="If Exchange provider is an external one Currency which only supported currencies are allowed /n",
        domain=[('exchange_currency', '=', True)], required=False)

    limit_negative = fields.Boolean('Limit - ?')
    limit_negative_value = fields.Float(
        'ValueLimit -', default=-500.0)

    limit_positive = fields.Boolean('Limit + ?')
    limit_positive_value = fields.Float(
        'Value Limit +', default=500.0)

    account_id = fields.Many2one('account.account', 'Related account', required=False,
                                 help='Related account for Odoo Accounting purpose')
    initcredit = fields.Float('Initial amount of currency',
                              help='Initial amount currency of User gets on this account')
    image = fields.Binary("Image", attachment=True,
                          help="This field holds the image used for this currency/account, limited to 1024x1024px")
    image_medium = fields.Binary("Medium-sized image",
                                 compute="_get_image", store=True, attachment=True,
                                 help="Medium-sized image of this currency/account. It is automatically " \
                                      "resized as a 128x128px image, with aspect ratio preserved. " \
                                      "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image",
                                compute="_get_image", store=True, attachment=True,
                                help="Small-sized image of this currency/account. It is automatically " \
                                     "resized as a 64x64px image, with aspect ratio preserved. " \
                                     "Use this field anywhere a small image is required.")
    exchange_rate = fields.Float(
        'Exchange Rate', related='currency_id.rate', readonly=True)

    #       readonly=True, digits=lambda cr:(16, 2))
    #       digits=dp.get_precision('Account')

    _sql_constraints = [
        ('name', 'unique(name)',
        'We can only have one line per name'),
        ('default_account', 'unique(membership_type,default_account,exchange_provider_id)',
        'We can only have one default account per type'),
    ]

    @api.depends('image')
    def _get_image(self):
        for record in self:
            if record.image:
                record.image_medium = image.crop_image(record.image, type='top', ratio=(4, 3), thumbnail_ratio=4)
                record.image_thumb = image.crop_image(record.image, type='top', ratio=(4, 3), thumbnail_ratio=6)
            else:
                record.image_medium = False
                record.image_thumb = False

# TODO    @api.one
#    @api.constrains('account_type', 'membership_type', 'default_account')
#    def _check_application(self):
#        """
#        Check that the Account are single then other as user accounts
#        """
#        if self.account_type != user
#                self.account_type.id:
#            raise except_orm(_('Data error!'),
#                             _("Only user accounts can have more than one per type"))
#        else
#                self.membership_type.id:
#            raise except_orm(_('Data error!'),
#                             _("Only one user accounts per type"))

    '''
    def update_all_partners(self):
        # Update balances on all partners
        partner_obj = self.pool.get('res.partner')
        partner_ids = partner_obj.search(cr, uid, [], context=context)
        partner_obj.update_wallet_balance(
            cr, uid, partner_ids, context=context
        )

    def create(self):
        # Mark the currency as wallet and then
        # update balance on all partners at creation
        self.pool.get('res.currency').write(
            cr, uid, [vals['currency_id']], {'exchange_currency': True},
            context=context
        )
        res = super(AccountTypesConfig, self).create(
            cr, uid, vals, context=context
        )
        self.update_all_partners(cr, uid, context=context)
        return res

    def write(self):
        # Update balance on all partners when modified
        res = super(AccountTypesConfig, self).write(
            cr, uid, ids, vals, context=context
        )
        self.update_all_partners(cr, uid, context=context)
        return res

    def unlink(self):
        # Remove the wallet flag on the currency
        # and then update balance on all partners
        for currency in self.browse(cr, uid, ids, context=context):
            self.pool.get('res.currency').write(
                cr, uid, [currency.currency_id.id],
                {'exchange_currency': False}, context=context
            )
        res = super(AccountTypesConfig, self).unlink(
            cr, uid, ids, context=context
        )
        self.update_all_partners(cr, uid, context=context)
        return res
    '''

