# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import models, fields, api
from openerp.exceptions import except_orm

#    List of Access Data for Distributed DB's


class DistributedDB(models.Model):
    _name = 'distributed.db.list'
    _description = 'Distributed DB Data'
    name = fields.Char('Name', size=64,required=True)

    description = fields.Text('Description')
    ip = fields.Char('IP', size=64, required=True)
    port = fields.Integer('port', required=True)
    db_hash = fields.Char('Hash of the DB')
    login = fields.Char('Loginname to external DB')
    pw = fields.Char('Password to external DB')
    use_keys = fields.Boolean(
        'Using keys?',
        help='Using keys instead of login/password?')
    private_key = fields.Text(
        'Private Key', required=True,
        default='XXXX')
    public_key = fields.Text(
        'Public Key', required=True,
        default='XXXX')
    goclouder = fields.Boolean(
        'Is a Goclouder Docker container?',
        help='Name of the Account')
#    clouder_container_ids = fields.One2many('clouder.container',
#                                            'container_id', 'Ports')
    active = fields.Boolean('Active?', default=True)

