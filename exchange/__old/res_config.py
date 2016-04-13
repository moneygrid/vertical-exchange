# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Lucas Huber, Copyright CoĐoo Project
#    based on account_wallet by Yannick Buron, Copyright Yannick Buron
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import logging

from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp


class ExchangeConfigSettings(orm.Model):


    # Add Exchange configuration (parameters) to Exchange settings
    _inherit = 'exchange.config.settings'

    _columns = {
        'name': fields.char(
            'Exchange Name',
            required=True,
            size=21,
            help='Name of the Exchange'
        ),
        'code': fields.char(
            'Exchange Code',
            required=False,
            default="GB WXYZ",
            size=7,
            help="Unique Exchange Code (EC)"
                 "First part of the 20 digits Account Code CC BBBB"
                 "CC country code -> DE Germany"
                 "BBBB Exchange code"
        ),
        'display_balance': fields.boolean('Everyone can see balances?'),
        'journal_id': fields.many2one(
            'account.journal', 'Community Journal', required=True
        ),
        'account_ids': fields.one2many(
            'exchange.config.accounts', 'config_id', 'Accounts templates'
#            domain=lambda self: [('name', '=', self._name)],
#            auto_join=True, string='Lines'
        ),

        # TODO is ev. not used anymore in the future
        'default_currency_id': fields.many2one(
            'res.currency', 'Default currency',
#            domain=[('wallet_currency', '=', True)], required=False
        ),
        'use_account_numbers': fields.boolean(
            'Use of Account Numbering System',
            help="Use of the 20 digits Account Numbering Code 'CC BBBB DDDDDDDD XXXX-KK'"
        ),
    }


class AccountTypesType(orm.Model):

   # Lines containing the a list accounts types
    _name = 'exchange.account.type'
    _description = 'Exchange Accounts Types list'
    _columns = {
        'name': fields.char(
            'Account Type Key', required=True, size=2, default="XX",
            help="Account key examples"
                 "PD Private User Default account"
                 "PU Private User sub-account"
                 "BD Business User Default account"
                 "BC Business User Credit account"
                 "SY System account"
        ),
        'account_name': fields.char(
            'Account name', size=32, required=True,
            translate=True, default='XY User account',
            help="Name of the Account"
        ),
        'account_desc': fields.char(
            'Account Type Description',required=False,
            help='Description'
        ),
    }


    _sql_constraints = [
        (
            'typename_unique', 'unique(name)',
            'We can only have one line per name'
        ),
        (
            'account_name_unique', 'unique(account_name)',
            'We can only have one line per key'
        )
    ]

class AccountTypesConfig(orm.Model):


    # Lines containing the general configuration for accounts types

    _name = 'exchange.config.accounts'
    _description = 'Exchange Account Type/Template configuration'
    _columns = {
        'name': fields.char(
            'Account Name', required=True, size=40, translate=True,
            help='Name of the Account'),

        'account_type': fields.selection([
                ('user', 'User account'),
                ('system', 'System account'),
                ('clearing', 'Clearing account'),
                ('rating', 'Rating account'),
            ], 'Account Type', readonly=False,
            required=True, default='user',
            help="Type of account /n"
                 "User Account, belongs to a user"
                 "System Account, belongs to the system or organisation"
                 "Clearing Account, belongs to the system or organisation"),

        'type_prefix': fields.many2one(
            'exchange.account.type', 'Account Number Prefix/Type', required=False, size=2,
            help="Prefix for Number of the Accounts"
                 "in last part of the 21 digits Account Code"),

        'config_id': fields.many2one(
            'exchange.config.settings', 'Config ID', required=True),

        'accounts_ids': fields.one2many(
            'exchange.accounts', 'template_id', 'Related accounts',
            help='Related accounts for transactions'),

        'hidden': fields.boolean(
            'Hidden Account',
            help='Account is hidden to users'),

        # TODO Filter on many2one about 'product.public.category' = Membership
        'membership_type': fields.many2one(
            'product.product', 'Type of membership', required=False,
            help='For this of membership the accounts will be used'),

        'default_account': fields.boolean(
            'Default Account',
            default=False,
            help='This account will be used/attached for new users of the group'),

        'currency_id': fields.many2one(
            'res.currency', 'Currency', required=True),

        'limit_negative': fields.boolean('Limit - ?'),
        'limit_negative_value': fields.float(
            'ValueLimit -', digits_compute=dp.get_precision('Product Price'),
            default=-500.0),

        'limit_positive': fields.boolean('Limit + ?'),
        'limit_positive_value': fields.float(
            'Value Limit +', digits_compute=dp.get_precision('Product Price'),
            default=500.0),

        'account_id': fields.many2one(
            'account.account', 'Related account', required=False,
            help='Related account for Odoo Accounting purpose'),

        'exchange_provider_id': fields.boolean(
            'External DB',
            help='Check if an outside transaction engine exists'),

        'external_ledger_id': fields.many2one(
            'distributed.db.list', 'External Ledger ID'),

        'initcredit': fields.float(
            'Initial amount of currency',
            help='Initial amount currency of User gets on this account'),
        'initcredit_type': fields.many2one(
            'exchange.transaction.type',
            'Initial credit transaction type'),
        # Related fields (not stored in DB)
        'currency_symbol': fields.related('currency_id',
            'symbol', string='Currency Symbol', type='many2one',
            relation='res.currency', readonly=True),
    }


    _sql_constraints = [
        (
            'name', 'unique(name)',
            'We can only have one line per name'
        )
    ]
    '''
    def update_all_partners(self, cr, uid, context=None):
        # Update balances on all partners
        partner_obj = self.pool.get('res.partner')
        partner_ids = partner_obj.search(cr, uid, [], context=context)
        partner_obj.update_wallet_balance(
            cr, uid, partner_ids, context=context
        )

    def create(self, cr, uid, vals, context=None):
        # Mark the currency as wallet and then
        # update balance on all partners at creation
        self.pool.get('res.currency').write(
            cr, uid, [vals['currency_id']], {'wallet_currency': True},
            context=context
        )
        res = super(AccountTypesConfig, self).create(
            cr, uid, vals, context=context
        )
        self.update_all_partners(cr, uid, context=context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        # Update balance on all partners when modified
        res = super(AccountTypesConfig, self).write(
            cr, uid, ids, vals, context=context
        )
        self.update_all_partners(cr, uid, context=context)
        return res

    def unlink(self, cr, uid, ids, context=None):
        # Remove the wallet flag on the currency
        # and then update balance on all partners
        for currency in self.browse(cr, uid, ids, context=context):
            self.pool.get('res.currency').write(
                cr, uid, [currency.currency_id.id],
                {'wallet_currency': False}, context=context
            )
        res = super(AccountTypesConfig, self).unlink(
            cr, uid, ids, context=context
        )
        self.update_all_partners(cr, uid, context=context)
        return res
    '''
