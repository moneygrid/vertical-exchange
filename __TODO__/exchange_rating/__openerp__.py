# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Lucas Huber, Copyright CoĐoo Project
#    based on vite by Yannick Buron, Copyright Yannick Buron
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

{
    'name': 'Exchange Rating API',
    'version': '1.0',
    'category': 'Social Network',
    'author': 'Yannick Buron',
    'license': 'AGPL-3',
    'description': """
Exchange Rating API
===================

Framework module for managing ratings inside Odoo
----------------------------------------------
    * Rating type configurable
    * Use base inherit config to modify rating types in category
    * Provide abstract class for implementing exchange_rating in your own classes
    * Votes are visible in object marked as "evaluated"
""",
    'website': 'https://github.com/YannickB/community-management',
    'depends': [
        'base',
        'base_community',
        'base_recursive_model',
        'membership_users'
    ],
    'data': [
        'security/ir.model.access.csv',
        'vote_view.xml',
        'res_config_view.xml'
    ],
    'installable': True,
}
