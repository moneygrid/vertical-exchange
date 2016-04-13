# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Base Exchange',
    'version': '9.0.0.1.x',
    'category': 'Community',
    'summary': 'Basic configuration & framework for distributed ledgers',
    'author': 'Lucas Huber',
    'license': 'LGPL-3',
    'description': """
Base Exchange
==============

Creates configuration menu for exchange modules
and framework for Exchange Providers (Multiwallet)

-----------------------------------------------------
""",
    'website': 'https://github.com/moneygrid/vertical-exchange',
    'depends': [
        'base',
        'mail',
        'association',
    ],
    'data': [
        'security/base_exchange_security.xml',
        'security/ir.model.access.csv',
        'views/exchange_provider_view.xml',
        'views/res_config_view.xml',
        'data/exchange_data.xml',
    ],
 #   'demo': ['base_community_demo.xml'],
    'installable': True,
}
