# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Exchange Provider Base',
    'version': '9.0.0.1.x',
    'category': 'Community',
    'summary': 'Basic framework for transaction engines',
    'author': 'Lucas Huber',
    'license': 'LGPL-3',
    'description': """
Exchange Provider Base
======================

Creates framework for Exchange Providers/ Transaction engines (Multiwallet)

-----------------------------------------------------
""",
    'website': 'https://github.com/moneygrid/vertical-exchange',
    'depends': [
        'base_exchange',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/exchange_provider_view.xml',
      #  'views/res_config_view.xml',
        'data/exchange_data.xml',
    ],
 #   'demo': ['base_community_demo.xml'],
    'installable': True,
}
