# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Lucas Huber, Copyright: CoĐoo Project
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

from openerp import models, fields, api
from openerp.exceptions import except_orm

#    List of Access Data for Distributed DB's

class DistributedDB(models.Model):
    _name = 'distributed.db.list'
    _description = 'Distributed DB Data'
    name = fields.Char('Name', size=64,required=True)
    config_id = fields.Many2one(
        'exchange.config.accounts', 'Config ID',
        help='If ledger are used for an exchange system')
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

