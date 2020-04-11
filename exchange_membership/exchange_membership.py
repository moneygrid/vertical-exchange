# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber, Yannick Buron>
# based on account_wallet by Yannick Buron, Copyright Yannick Buron
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
# from lxml import etree
# from lxml.builder import E
from odoo import models, fields, api


class ResPartner(models.Model):

    """
    Add some field in partner to use for Exchange
    """

    _inherit = 'res.partner'

    presentation = fields.Text('About me/us')
    show_phone = fields.Boolean('Show phone to others members?')
    exchange_group = fields.Selection([
        ('user', 'User'),
        ('broker', 'Broker'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
        ],
        readonly=True, track_visibility='onchange',
        help="Role of User in Exchange")
    # TODO     related = 'res.users.membership_state',

    state = fields.Selection([
        ('application', 'Application'),
        ('open', 'Active'),
        ('blocked', 'Blocked'),
        ('closed', 'Closed'),
        ], 'Membership Status', readonly=False,
        required=True, default='open', track_visibility='onchange',
        help="Status of Account"
             "Blocked, for temporary blocking transactions")

    membership_type = fields.Many2one('product.product',
                                      'Membership Type', related='member_lines.membership_id',
                                      readonly=True, store=True, help="Membership Type from Products")
    membership_state2 = fields.Selection(related='partner_id.membership_state', string='Membership State',
                                         store=False, readonly=True),
    # TODO should be the same value as in 'membership_state'

    @api.multi
    def _membership_type(self):
        self.ensure_one()  # One record expected, raise error if self is an unexpected recordset
        return 'TODO1'

    """
    @api.one
    def _member_state(self, ids):
        res = {}
        for id in ids:
            record = self.browse()
            res.update({id: record.membership_state})
            #  res = self.membership_state
        return res
    """
    @api.one
    def do_membership_deblock(self):
        self.state = 'open'

    @api.one
    def do_membership_block(self):
        self.state = 'blocked'

    @api.one
    def do_membership_close(self):
        self.state = 'closed'

    @api.onchange('res.users.groups_id')
    def _get_user_role(self):
        # Control the access rights of the current user

        if self.pool.get('res.users').has_group(
                'base_exchange.group_exchange_user'):
                self.exchange_group = 'user'
        if self.pool.get('res.users').has_group(
                'base_exchange.group_exchange_moderator'):
                self.exchange_group = 'moderator'
        if self.pool.get('res.users').has_group(
                'base_exchange.group_exchange_admin'):
                self.exchange_group = 'admin'
        return
