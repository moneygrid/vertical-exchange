# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Base Exchange',
    'version': '0.0.1.x',
    'category': 'Community',
    'summary': 'Basic configuration',
    'author': 'Lucas Huber',
    'license': 'LGPL-3',
    'description': """
Base Exchange
==============

- Creates configuration menu for exchange modules
- Creates all basic models for exchange
- Creates menus in Accounting Configuration
-------------------------------------------------
""",
    'website': 'https://github.com/moneygrid/vertical-exchange',
    'depends': [
        'base',
        'mail',
        'account_accountant',
    ],
    'data': [
        'security/base_exchange_security.xml',
        'security/ir.model.access.csv',
        'views/res_config_view.xml',
        'data/exchange_data.xml',
    ],
    'installable': True,
}
